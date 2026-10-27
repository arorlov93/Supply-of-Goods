/* Приём заявок с сайта. Cloudflare Pages Function, адрес /api/quote.
 *
 * Порядок такой: сначала заявка пишется в базу D1, потом уходит письмо.
 * Запись раньше письма не случайна: письмо зависит от чужой службы, а база
 * нет, и потерять обращение из-за чужого сбоя нельзя.
 *
 * Письмо уходит через Resend, ключ из переменной окружения RESEND_KEY,
 * заданной в настройках проекта Pages. Ключа в репозитории нет и быть не
 * должно. Пока ключа нет, письмо идёт через бесплатный ретранслятор, у
 * которого есть предел частоты, см. ниже.
 */

import { relay, markMailed, payloadFor } from "../_queue.js";

const FIELDS = ["name", "mail", "co", "country", "cat", "terms", "qty", "dest", "spec"];
const LABEL = {
  name: "Name", mail: "Work e-mail", co: "Company", country: "Country",
  cat: "Category", terms: "Terms to quote", qty: "Quantity",
  dest: "Destination", spec: "Specification",
};

export async function onRequestPost(ctx) {
  try {
    return await handle(ctx);
  } catch (e) {
    console.log("quote handler threw", String(e && e.stack || e).slice(0, 400));
    return json({ ok: false, code: "server_error" }, 500);
  }
}

async function handle(ctx) {
  const { request, env } = ctx;
  let d;
  try {
    d = await request.json();
  } catch {
    return json({ ok: false, code: "bad_json" }, 400);
  }

  /* Подтверждение от браузера: «я уведомление отправил».
     Ретранслятор принимает письма только из настоящего браузера, запросы
     с серверов Cloudflare он отбивает кодом 429 (проверено: в ту же
     секунду с обычной машины отвечает 200). Поэтому письмо шлёт
     страница, а сюда возвращает отметку, чтобы в CRM было видно
     действительное положение дел, а не «в очереди» навсегда.

     Отметка подписана: иначе любой мог бы пометить чужие заявки
     отправленными и спрятать их от дожима. Подпись короткая, её цена
     ошибки невелика: максимум не уйдёт одно повторное уведомление. */
  if (d && d.confirm) {
    const ok = await signOk(env, d.confirm, d.token);
    if (!ok) return json({ ok: false, code: "bad_token" }, 403);
    await markMailed(env, parseInt(d.confirm, 10));
    return json({ ok: true, confirmed: true });
  }

  // обязательный минимум: кто пишет, куда отвечать и что нужно
  for (const k of ["name", "mail", "spec"]) {
    if (!d[k] || !String(d[k]).trim()) {
      return json({ ok: false, code: "missing", field: k }, 400);
    }
  }
  if (!/^[^@\s]+@[^@\s.]+\.[^@\s]+$/.test(String(d.mail).trim())) {
    return json({ ok: false, code: "bad_email" }, 400);
  }
  // защита от мусора: ни одно поле не длиннее разумного
  for (const k of FIELDS) {
    if (d[k] != null && String(d[k]).length > 4000) {
      return json({ ok: false, code: "too_long", field: k }, 400);
    }
  }
  // ловушка для ботов: поле скрыто стилями, человек его не заполняет
  if (d.website) return json({ ok: true });


  const esc = (s) =>
    String(s ?? "").replace(/[<>&"]/g, (c) =>
      ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }[c])
    );

  const rows = FIELDS.filter((k) => d[k] && String(d[k]).trim())
    .map(
      (k) =>
        `<tr><td style="padding:5px 14px 5px 0;color:#667;vertical-align:top;white-space:nowrap">` +
        `<b>${LABEL[k]}</b></td><td style="padding:5px 0">${esc(d[k]).replace(/\n/g, "<br>")}</td></tr>`
    )
    .join("");

  const text = FIELDS.filter((k) => d[k] && String(d[k]).trim())
    .map((k) => `${LABEL[k]}: ${d[k]}`)
    .join("\n");

  const meta = [
    `Page: ${String(d.page || "").slice(0, 200)}`,
    `Country (Cloudflare): ${request.headers.get("cf-ipcountry") || "unknown"}`,
    `Received: ${new Date().toISOString()}`,
  ].join("\n");

  /* Заявка кладётся в базу раньше письма: если почта почему-либо не
     уйдёт, сама заявка всё равно не потеряется и будет видна в /crm.
     Ошибка записи не должна ронять ответ посетителю, поэтому она только
     попадает в журнал, а человек получает обычное подтверждение. */
  let saved = false;
  let leadId = null;
  if (env.DB) {
    try {
      const res = await env.DB.prepare(
        `INSERT INTO leads (created,name,mail,co,country,cat,terms,qty,dest,spec,page,ip_country,status)
         VALUES (?,?,?,?,?,?,?,?,?,?,?,?,'new')`
      ).bind(
        new Date().toISOString(),
        ...FIELDS.map((k) => (d[k] != null && String(d[k]).trim() ? String(d[k]) : null)),
        String(d.page || ""),
        request.headers.get("cf-ipcountry") || null
      ).run();
      saved = true;
      leadId = (res && res.meta && res.meta.last_row_id) || null;
    } catch (e) {
      console.log("d1 insert failed", String(e && e.message || e).slice(0, 200));
    }
  }

  const TO = env.QUOTE_TO || "info@ispgroupgc.com";

  /* Без ключа Resend письмо уходит через ретранслятор, которому не нужна ни
     регистрация, ни DNS: адрес получателя остаётся на сервере и в браузер не
     попадает. Как только в переменных окружения появится RESEND_KEY, письма
     пойдут с собственного домена, и эта ветка перестанет использоваться. */
  if (!env.RESEND_KEY) {
    const payload = payloadFor({
      ...d,
      page: String(d.page || "/"),
      ip_country: request.headers.get("cf-ipcountry") || "unknown",
    });

    const first = await relay(TO, payload);
    if (first.ok) {
      await markMailed(env, leadId);
      return json({ ok: true, via: "relay", saved });
    }
    console.log("relay failed", first.status, first.detail);

    /* Ретранслятор пропускает примерно одну заявку в сорок секунд, на
       вторую подряд отвечает 429. Замерено тремя попытками с шагом в
       двадцать секунд: 200, 429, 200.

       Повтор прямо здесь не работает: среда не держит фоновую задачу с
       длинной паузой, это тоже проверено на живом сайте, письмо так и
       не уходило. Поэтому заявка просто остаётся в базе с отметкой
       mailed = 0, а добирает её отдельный Worker раз в минуту, см.
       mailer/worker.js. Для посетителя это успех, потому что заявка у
       нас, и письмо придёт с опозданием максимум на минуту. */
    return saved
      ? json({ ok: true, saved: true, mail: "queued", id: leadId, token: await sign(env, leadId) })
      : json({ ok: false, code: "mail_failed", status: first.status }, 502);
  }

  let r;
  try {
    r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: env.QUOTE_FROM || "ISP Group Site <quotes@ispgroupgc.com>",
        to: [TO],
        reply_to: String(d.mail).trim(),
        subject: `Quote request: ${d.co || d.name}${d.country ? " / " + d.country : ""}`,
        html: `<h3 style="font:600 16px system-ui">New quote request</h3>
<table style="font:14px/1.5 system-ui;border-collapse:collapse">${rows}</table>
<pre style="font:12px/1.5 ui-monospace;color:#889;margin-top:18px">${esc(meta)}</pre>`,
        text: text + "\n\n" + meta,
      }),
    });
  } catch {
    return saved ? json({ ok: true, saved: true, mail: false })
                 : json({ ok: false, code: "upstream_unreachable" }, 502);
  }

  if (!r.ok) {
    const detail = (await r.text().catch(() => "")).slice(0, 300);
    console.log("resend failed", r.status, detail);
    /* Как и с ретранслятором: отметка остаётся в нуле, заявку доберёт
       mailer/worker.js. Сетка нужна любому отправителю, не только
       бесплатному. */
    return saved
      ? json({ ok: true, saved: true, mail: "queued", id: leadId, token: await sign(env, leadId) })
      : json({ ok: false, code: "mail_failed", status: r.status }, 502);
  }

  await markMailed(env, leadId);
  return json({ ok: true, saved });
}

export async function onRequestGet() {
  return json({ ok: false, code: "post_only" }, 405);
}

/* Подпись к номеру заявки. Ключ тот же, что у CRM: отдельный заводить
   незачем, оба служат одному, не пускать посторонних к чужим заявкам. */
async function sign(env, id) {
  const secret = env.CRM_SECRET || "";
  if (!secret) return null;
  const key = await crypto.subtle.importKey(
    "raw", new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
  );
  const mac = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode("lead:" + id));
  return [...new Uint8Array(mac)].slice(0, 12).map((b) => b.toString(16).padStart(2, "0")).join("");
}

/* Сравнение без ранних выходов: по времени ответа подпись не подбирается. */
async function signOk(env, id, given) {
  const want = await sign(env, id);
  if (!want || typeof given !== "string" || given.length !== want.length) return false;
  let diff = 0;
  for (let i = 0; i < want.length; i++) diff |= want.charCodeAt(i) ^ given.charCodeAt(i);
  return diff === 0;
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}
