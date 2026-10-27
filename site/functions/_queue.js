/* Очередь писем по заявкам. Общий код для приёма заявки и для дожима.
 *
 * Зачем очередь. Заявка пишется в базу раньше письма, потому что письмо
 * зависит от чужой службы, а база нет. У бесплатного ретранслятора предел
 * примерно одна заявка в сорок секунд, на вторую подряд он отвечает 429,
 * это замерено на живом сайте. Значит, часть писем не уйдёт с первой
 * попытки, и нужен кто-то, кто дошлёт.
 *
 * Повтор прямо в запросе не работает: среда не держит фоновую задачу с
 * длинной паузой, проверено, письмо так и не ушло. Правильное место для
 * дожима это расписание, то есть отдельный Worker с Cron (он написан,
 * mailer/worker.js). Пока у ключа нет прав на такой Worker, дожим висит
 * на обычных обращениях к сайту: страницу кто-то открыл, заодно ушло
 * одно отложенное письмо. Посетитель этого не ждёт, всё идёт после
 * ответа.
 *
 * Отметка mailed: 0 ждёт отправки, 1 отправлено, 2 отправляется прямо
 * сейчас. Двойка нужна против двойных писем: страницу могут открыть два
 * человека одновременно, и без захвата оба возьмут одну и ту же заявку.
 * Захват делается одним оператором UPDATE ... RETURNING, то есть он
 * неделим, и заявка достаётся ровно одному.
 */

const FIELDS = ["name", "mail", "co", "country", "cat", "terms", "qty", "dest", "spec"];
const LABEL = {
  name: "Name", mail: "Work e-mail", co: "Company", country: "Country",
  cat: "Category", terms: "Terms to quote", qty: "Quantity",
  dest: "Destination", spec: "Specification",
};

export function payloadFor(row) {
  return {
    _subject: `Quote request: ${row.co || row.name}${row.country ? " / " + row.country : ""}`,
    _replyto: row.mail || "",
    _template: "table",
    _captcha: "false",
    ...Object.fromEntries(
      FIELDS.filter((k) => row[k] && String(row[k]).trim()).map((k) => [LABEL[k], String(row[k])])
    ),
    Origin_page: row.page || "/",
    Visitor_country: row.ip_country || "unknown",
    ...(row.created ? { Received: row.created } : {}),
  };
}

/* Одна попытка отправки. Заголовок Origin ставить нельзя: среда Worker
   его запрещает и бросает исключение. Ретранслятору достаточно Referer. */
export async function relay(to, payload) {
  try {
    const r = await fetch("https://formsubmit.co/ajax/" + encodeURIComponent(to), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Referer: "https://ispgroupgc.com/",
      },
      body: JSON.stringify(payload),
    });
    const body = await r.json().catch(() => ({}));
    return {
      ok: r.ok && String(body.success) === "true",
      status: r.status,
      detail: JSON.stringify(body).slice(0, 200),
    };
  } catch (e) {
    return { ok: false, status: 0, detail: String((e && e.message) || e).slice(0, 200) };
  }
}

export async function markMailed(env, id) {
  if (!env.DB || !id) return;
  try {
    await env.DB.prepare("UPDATE leads SET mailed = 1 WHERE id = ?").bind(id).run();
  } catch (e) {
    const m = String((e && e.message) || e);
    if (!/no such column/i.test(m)) console.log("mark mailed failed", m.slice(0, 160));
  }
}

/* Колонки mailed может ещё не быть: база старше очереди. SQLite не умеет
   ADD COLUMN IF NOT EXISTS, поэтому пробуем и глотаем ошибку повторного
   добавления.

   Старые заявки помечаем отправленными, иначе первый же запуск вышлет
   заново всё, что накопилось. Но не все подряд: заявка, пришедшая прямо
   сейчас, во время выкладки, ещё ждёт своего письма, и пометить её
   отправленной значит потерять ровно то, ради чего очередь и делалась.
   Граница по времени: четверть часа, за это время судьба письма уже
   решилась в ту или иную сторону. */
async function ensureColumn(env) {
  try {
    await env.DB.prepare("ALTER TABLE leads ADD COLUMN mailed INTEGER NOT NULL DEFAULT 0").run();
    const r = await env.DB.prepare("UPDATE leads SET mailed = 1 WHERE created < ?")
      .bind(new Date(Date.now() - 15 * 60000).toISOString()).run();
    console.log("колонка mailed заведена, прошлых заявок помечено:", (r && r.meta && r.meta.changes) || 0);
  } catch (e) {
    const m = String((e && e.message) || e);
    if (!/duplicate column/i.test(m)) {
      console.log("миграция mailed не прошла:", m.slice(0, 160));
      return false;
    }
  }
  return true;
}

/* Выдержка между попытками. Без неё дожим на оживлённом сайте просто
   молотит в предел частоты: замерено, два захода подряд дали два отказа
   429 по одной и той же заявке. Шестьдесят секунд с запасом над
   измеренными сорока.

   Проверка и отметка времени делаются одним оператором UPDATE, и право
   на попытку получает тот, чей UPDATE изменил строку. Иначе два
   одновременных захода оба прочитают старое время и оба пойдут
   стучаться. */
const PACE_MS = 60000;

async function mayTry(env) {
  try {
    await env.DB.prepare("CREATE TABLE IF NOT EXISTS queue_meta (k TEXT PRIMARY KEY, v TEXT)").run();
    const now = new Date().toISOString();
    const cutoff = new Date(Date.now() - PACE_MS).toISOString();
    const r = await env.DB
      .prepare("UPDATE queue_meta SET v = ? WHERE k = 'last_try' AND v < ?")
      .bind(now, cutoff).run();
    const touched = (r && r.meta && (r.meta.changes ?? r.meta.rows_written)) || 0;
    if (touched >= 1) return true;
    /* Строки ещё нет: заводим. INSERT OR IGNORE делает попытку первой
       только для одного захода, остальные получат ноль изменений. */
    const ins = await env.DB
      .prepare("INSERT OR IGNORE INTO queue_meta (k, v) VALUES ('last_try', ?)")
      .bind(now).run();
    return !!(ins && ins.meta && ins.meta.changes === 1);
  } catch (e) {
    console.log("выдержка не сработала:", String((e && e.message) || e).slice(0, 160));
    return false;
  }
}

/* Отправляет не больше одной отложенной заявки. Больше одной за раз
   бессмысленно: следующая всё равно упрётся в предел частоты. */
export async function drainOne(env) {
  if (!env.DB) return { ok: false, reason: "no_database" };

  /* Без ключа Resend дожимать нечем. Бесплатный ретранслятор не принимает
     запросы с серверов Cloudflare: три попытки с интервалом в минуту
     получили 429, а запрос с обычной машины секундой позже получил 200.
     Это свойство ретранслятора, а не предел частоты, и обойти его с
     сервера нельзя. Пока ключа нет, уведомление отправляет сама
     страница, а заявка в любом случае лежит в базе и видна в CRM.

     Появится ключ, и этот дожим станет настоящей сеткой: он разошлёт
     всё, что накопилось с отметкой ноль, включая заявки тех посетителей,
     у кого вкладка закрылась раньше, чем ушло уведомление. */
  if (!env.RESEND_KEY) return { ok: true, sent: 0, note: "уведомление шлёт страница" };

  if (!(await ensureColumn(env))) return { ok: false, reason: "no_column" };
  if (!(await mayTry(env))) return { ok: true, sent: 0, note: "выдержка" };

  let row;
  try {
    /* Захват и чтение одним оператором: заявка достаётся ровно одному
       обращению, даже если их пришло несколько сразу. Двойка держится
       не дольше минуты, чтобы оборванная попытка не заперла заявку
       навсегда. */
    const res = await env.DB.prepare(
      `UPDATE leads SET mailed = 2
        WHERE id = (
          SELECT id FROM leads
           WHERE COALESCE(mailed,0) = 0
              OR (mailed = 2 AND claimed < ?)
           ORDER BY id ASC LIMIT 1)
        RETURNING *`
    ).bind(new Date(Date.now() - 60000).toISOString()).first();
    row = res || null;
  } catch (e) {
    /* Колонки claimed может не быть на старой базе: заводим и выходим,
       следующее обращение уже пройдёт по быстрому пути. */
    const m = String((e && e.message) || e);
    if (/no such column: claimed/i.test(m)) {
      try {
        await env.DB.prepare("ALTER TABLE leads ADD COLUMN claimed TEXT").run();
      } catch {}
      return { ok: true, sent: 0, note: "claimed заведена" };
    }
    console.log("захват заявки не прошёл:", m.slice(0, 160));
    return { ok: false, reason: "db_error" };
  }

  if (!row) return { ok: true, sent: 0 };

  await env.DB.prepare("UPDATE leads SET claimed = ? WHERE id = ?")
    .bind(new Date().toISOString(), row.id).run().catch(() => {});

  const to = env.QUOTE_TO || "info@ispgroupgc.com";
  const r = await viaResend(env, to, row);

  if (r.ok) {
    await env.DB.prepare("UPDATE leads SET mailed = 1 WHERE id = ?").bind(row.id).run();
    console.log("заявка", row.id, "отправлена дожимом");
    return { ok: true, sent: 1, id: row.id };
  }

  /* Не ушло: возвращаем в очередь, а не теряем. */
  await env.DB.prepare("UPDATE leads SET mailed = 0 WHERE id = ?").bind(row.id).run();
  console.log("дожим не прошёл по заявке", row.id, r.status, r.detail);
  return { ok: false, id: row.id, status: r.status };
}

/* Отправка с собственного домена. Сюда дожим приходит только когда ключ
   задан, поэтому запасных веток здесь нет. */
async function viaResend(env, to, row) {
  const text = FIELDS.filter((k) => row[k] && String(row[k]).trim())
    .map((k) => `${LABEL[k]}: ${row[k]}`)
    .join("\n");
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: env.QUOTE_FROM || "ISP Group Site <quotes@ispgroupgc.com>",
        to: [to],
        reply_to: row.mail || undefined,
        subject: `Quote request: ${row.co || row.name}${row.country ? " / " + row.country : ""}`,
        text: `${text}\n\nPage: ${row.page || "/"}\nCountry: ${row.ip_country || "unknown"}\nReceived: ${row.created || ""}`,
      }),
    });
    if (r.ok) return { ok: true, status: r.status, detail: "" };
    return { ok: false, status: r.status, detail: (await r.text().catch(() => "")).slice(0, 160) };
  } catch (e) {
    return { ok: false, status: 0, detail: String((e && e.message) || e).slice(0, 160) };
  }
}
