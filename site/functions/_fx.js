/* Курсы ЕЦБ прямо в ответе сервера.
 *
 * Зачем это вообще понадобилось. Ежедневная часть страницы индекса
 * собиралась на машине и уезжала выкладкой. Выкладка требует токена
 * Cloudflare, токен живёт только в той сессии, которой его дали, а
 * расписание запускается в новой. То есть ежедневное обновление упиралось
 * не в код, а в то, что некому нажать кнопку.
 *
 * Здесь кнопка не нужна. Функции Pages стоят перед каждым запросом к
 * сайту. Значит, свежие курсы можно подставить в HTML по дороге к
 * читателю, и выкладывать для этого ничего не надо. Заодно это честнее по
 * сути: страница перестаёт быть снимком вчерашнего дня и становится тем,
 * чем притворялась.
 *
 * Поисковик и языковая модель видят ровно то же, что человек: подстановка
 * идёт в разметку на сервере, а не скриптом в браузере.
 *
 * Чего здесь намеренно нет.
 *
 * Ожидания. Ответ посетителю никогда не ждёт ЕЦБ. Если свежих курсов в
 * кэше нет, страница уходит с теми, что запечены при сборке, а поход за
 * новыми происходит после ответа. Следующий посетитель получит свежие.
 * Чужая служба не должна уметь замедлить наш сайт.
 *
 * Разбора XML библиотекой. В среде Worker её нет, а формат у ЕЦБ простой
 * и стабильный пятнадцать лет: два уровня одинаковых тегов. Регулярное
 * выражение здесь надёжнее, чем зависимость.
 */

const URL_ECB = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml";
const KEY = "https://fx.internal/ecb-90d";
const TTL = 6 * 3600;          // курсы меняются раз в сутки, шесть часов с запасом
const BACK = 22;               // торговых дней в месяце, примерно

// Валюты, в которых продавцы на наших коридорах выставляют счёт.
const WANT = [
  ["EUR", "European Union, Poland in euro contracts"],
  ["CNY", "China"],
  ["TRY", "Türkiye"],
  ["PLN", "Poland"],
  ["INR", "India"],
  ["KRW", "Korea"],
];

function parse(xml) {
  const days = [];
  const re = /<Cube\s+time=['"]([\d-]+)['"]\s*>([\s\S]*?)<\/Cube>/g;
  let m;
  while ((m = re.exec(xml))) {
    const rates = {};
    const inner = /<Cube\s+currency=['"]([A-Z]{3})['"]\s+rate=['"]([\d.]+)['"]/g;
    let k;
    while ((k = inner.exec(m[2]))) rates[k[1]] = parseFloat(k[2]);
    days.push({ date: m[1], rates });
  }
  return days;
}

function rows(days) {
  if (days.length < 2) return null;
  const today = days[0];
  const past = days[Math.min(BACK, days.length - 1)];
  // ЕЦБ даёт, сколько единиц валюты в одном евро. Покупателю нужно
  // обратное и в долларах: сколько долларов стоит единица валюты продавца.
  const usd = (t, code) =>
    code === "EUR" ? t.rates.USD
      : (t.rates.USD && t.rates[code] ? t.rates.USD / t.rates[code] : null);
  const out = [];
  for (const [code, who] of WANT) {
    const a = usd(today, code), b = usd(past, code);
    if (!a || !b) continue;
    out.push({ code, who, usd: a, change: ((a - b) / b) * 100 });
  }
  return out.length ? { date: today.date, compared_to: past.date, rows: out } : null;
}

async function pull() {
  const r = await fetch(URL_ECB, { cf: { cacheTtl: TTL } });
  if (!r.ok) throw new Error("ecb " + r.status);
  const fx = rows(parse(await r.text()));
  if (!fx) throw new Error("ecb: не разобрал");
  return fx;
}

/* Берём из кэша. Промах не ждём: возвращаем null, а поход за свежими
   вешаем на waitUntil. */
export async function fxCached(ctx) {
  const cache = caches.default;
  const req = new Request(KEY);
  const hit = await cache.match(req);
  if (hit) {
    try {
      return await hit.json();
    } catch {
      /* битая запись, перезапишем ниже */
    }
  }
  if (typeof ctx.waitUntil === "function") {
    ctx.waitUntil(
      pull()
        .then((fx) =>
          cache.put(
            req,
            new Response(JSON.stringify(fx), {
              headers: {
                "content-type": "application/json",
                "cache-control": "public, max-age=" + TTL,
              },
            })
          )
        )
        .catch((e) => console.log("fx: не обновил,", String(e).slice(0, 120)))
    );
  }
  return null;
}

function esc(s) {
  return String(s).replace(/[<>&]/g, (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" }[c]));
}

export function fxHtml(fx) {
  const body = fx.rows
    .map((r) => {
      const v = r.usd.toFixed(6).replace(/0+$/, "").replace(/\.$/, "");
      const ch = (r.change >= 0 ? "+" : "") + r.change.toFixed(2);
      return `<tr><td>${esc(r.code)}</td><td>${esc(r.who)}</td>` +
             `<td>$${v}</td><td><b>${ch}%</b></td></tr>`;
    })
    .join("");
  return (
    '<div class="tablewrap"><table class="lpi"><thead><tr>' +
    "<th>Currency</th><th>Sellers who invoice in it</th>" +
    "<th>One unit, in dollars</th><th>Change over a month</th>" +
    `</tr></thead><tbody>${body}</tbody></table></div>` +
    `<p class="pnote">European Central Bank reference rates for ${esc(fx.date)}, ` +
    `against ${esc(fx.compared_to)}. The bank publishes on working days only, so ` +
    "over a weekend this shows the last published day rather than today: the date " +
    "here is the date of the figures, not the date we fetched them.</p>"
  );
}

/* Подстановка в готовый ответ. Если свежего нет, ответ не трогаем: на
   странице остаётся то, что запечено при сборке, с честной датой. */
export function withFx(response, fx) {
  return new HTMLRewriter()
    .on("#fx-live", {
      element(el) {
        el.setInnerContent(fxHtml(fx), { html: true });
      },
    })
    .transform(response);
}
