/* Приём заявок с сайта. Cloudflare Pages Function, адрес /api/quote.
 *
 * Письмо уходит через Resend. Ключ берётся из переменной окружения RESEND_KEY,
 * заданной в настройках проекта Pages. Ключа в репозитории нет и быть не должно.
 *
 * Если ключ не задан, функция отвечает 503 и кодом "not_configured": фронтенд
 * показывает посетителю готовый текст заявки и адрес почты, а не молчит.
 */

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

async function handle({ request, env }) {
  let d;
  try {
    d = await request.json();
  } catch {
    return json({ ok: false, code: "bad_json" }, 400);
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

  const TO = env.QUOTE_TO || "info@ispgroupgc.com";

  /* Без ключа Resend письмо уходит через ретранслятор, которому не нужна ни
     регистрация, ни DNS: адрес получателя остаётся на сервере и в браузер не
     попадает. Как только в переменных окружения появится RESEND_KEY, письма
     пойдут с собственного домена, и эта ветка перестанет использоваться. */
  if (!env.RESEND_KEY) {
    let rr;
    try {
      rr = await fetch("https://formsubmit.co/ajax/" + encodeURIComponent(TO), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          // Origin ставить нельзя: среда Worker запрещает этот заголовок и
          // бросает исключение. Ретранслятору достаточно Referer.
          Referer: "https://ispgroupgc.com/",
        },
        body: JSON.stringify({
          _subject: `Quote request: ${d.co || d.name}${d.country ? " / " + d.country : ""}`,
          _replyto: String(d.mail).trim(),
          _template: "table",
          _captcha: "false",
          ...Object.fromEntries(
            FIELDS.filter((k) => d[k] && String(d[k]).trim()).map((k) => [LABEL[k], String(d[k])])
          ),
          Origin_page: String(d.page || "/"),
          Visitor_country: request.headers.get("cf-ipcountry") || "unknown",
        }),
      });
    } catch {
      return json({ ok: false, code: "upstream_unreachable" }, 502);
    }
    const body = await rr.json().catch(() => ({}));
    if (rr.ok && String(body.success) === "true") return json({ ok: true, via: "relay" });
    console.log("relay failed", rr.status, JSON.stringify(body).slice(0, 200));
    return json({ ok: false, code: "mail_failed", status: rr.status }, 502);
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
    return json({ ok: false, code: "upstream_unreachable" }, 502);
  }

  if (!r.ok) {
    const detail = (await r.text().catch(() => "")).slice(0, 300);
    console.log("resend failed", r.status, detail);
    return json({ ok: false, code: "mail_failed", status: r.status }, 502);
  }

  return json({ ok: true });
}

export async function onRequestGet() {
  return json({ ok: false, code: "post_only" }, 405);
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}
