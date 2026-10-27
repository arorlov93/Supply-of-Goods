/* Дожим писем по заявкам. Отдельный Worker с запуском раз в минуту.
 *
 * Зачем он нужен. Заявка с сайта сначала пишется в базу, потом уходит
 * письмом. Письмо зависит от чужой службы, и эта служба отказывает: у
 * бесплатного ретранслятора предел примерно одна заявка в сорок секунд,
 * на вторую подряд он отвечает 429. Замерено на живом сайте. Отправлять
 * повтор прямо в запросе нельзя: среда Worker не держит фоновую задачу
 * с длинной паузой, проверено, письмо так и не уходило.
 *
 * Поэтому очередь. В таблице есть отметка mailed. Функция приёма ставит
 * её в единицу, когда письмо ушло сразу. Всё, что осталось в нуле, этот
 * Worker добирает: раз в минуту берёт самую старую неотправленную заявку
 * и отправляет ровно одну. Одна в минуту заведомо ниже чужого предела,
 * поэтому дожим не спорит с ним, а ждёт.
 *
 * Свойство, ради которого всё затевалось: заявка не теряется никогда.
 * Худшее, что может случиться, это письмо на минуту позже.
 *
 * Появится RESEND_KEY, письма пойдут с нашего домена и сразу, а этот
 * Worker останется сеткой под теми случаями, когда и Resend ответит
 * отказом. Такая сетка нужна любому отправителю, не только бесплатному.
 */

const FIELDS = ["name", "mail", "co", "country", "cat", "terms", "qty", "dest", "spec"];
const LABEL = {
  name: "Name", mail: "Work e-mail", co: "Company", country: "Country",
  cat: "Category", terms: "Terms to quote", qty: "Quantity",
  dest: "Destination", spec: "Specification",
};

export default {
  async scheduled(event, env) {
    await drain(env);
  },

  /* Ручной запуск для проверки. Без ключа не отвечает ничем полезным,
     чтобы адрес Worker нельзя было использовать как кнопку рассылки. */
  async fetch(request, env) {
    const key = request.headers.get("x-drain-key");
    if (!env.DRAIN_KEY || key !== env.DRAIN_KEY) {
      return new Response("not found", { status: 404 });
    }
    const r = await drain(env);
    return new Response(JSON.stringify(r), {
      headers: { "content-type": "application/json; charset=utf-8" },
    });
  },
};

async function drain(env) {
  if (!env.DB) return { ok: false, reason: "no_database" };

  /* Колонка могла ещё не появиться: база старше этого Worker. SQLite не
     умеет ADD COLUMN IF NOT EXISTS, поэтому пробуем и глотаем ошибку
     повторного добавления.

     Старые заявки помечаем отправленными, иначе первый запуск вышлет
     пачку заново. Но только старше четверти часа: заявка, пришедшая
     прямо сейчас, ещё ждёт письма, и пометить её значит потерять то,
     ради чего очередь и заводилась. */
  try {
    await env.DB.prepare("ALTER TABLE leads ADD COLUMN mailed INTEGER NOT NULL DEFAULT 0").run();
    const r = await env.DB.prepare("UPDATE leads SET mailed = 1 WHERE created < ?")
      .bind(new Date(Date.now() - 15 * 60000).toISOString()).run();
    console.log("добавлена колонка mailed, прошлых заявок помечено:", (r && r.meta && r.meta.changes) || 0);
  } catch (e) {
    const m = String((e && e.message) || e);
    if (!/duplicate column/i.test(m)) console.log("миграция не прошла:", m.slice(0, 160));
  }

  let row;
  try {
    row = await env.DB
      .prepare("SELECT * FROM leads WHERE COALESCE(mailed,0) = 0 ORDER BY id ASC LIMIT 1")
      .first();
  } catch (e) {
    console.log("чтение очереди не прошло:", String((e && e.message) || e).slice(0, 160));
    return { ok: false, reason: "db_error" };
  }

  if (!row) return { ok: true, sent: 0 };

  const TO = env.QUOTE_TO || "info@ispgroupgc.com";
  const sent = env.RESEND_KEY ? await viaResend(env, TO, row) : await viaRelay(TO, row);

  if (!sent.ok) {
    console.log("заявка", row.id, "не ушла:", sent.status, sent.detail);
    return { ok: false, id: row.id, status: sent.status };
  }

  await env.DB.prepare("UPDATE leads SET mailed = 1 WHERE id = ?").bind(row.id).run();
  console.log("заявка", row.id, "отправлена дожимом");
  return { ok: true, sent: 1, id: row.id };
}

function pairs(row) {
  return FIELDS.filter((k) => row[k] && String(row[k]).trim())
    .map((k) => [LABEL[k], String(row[k])]);
}

async function viaRelay(to, row) {
  try {
    const r = await fetch("https://formsubmit.co/ajax/" + encodeURIComponent(to), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Referer: "https://ispgroupgc.com/",
      },
      body: JSON.stringify({
        _subject: `Quote request: ${row.co || row.name}${row.country ? " / " + row.country : ""}`,
        _replyto: row.mail || "",
        _template: "table",
        _captcha: "false",
        ...Object.fromEntries(pairs(row)),
        Origin_page: row.page || "/",
        Visitor_country: row.ip_country || "unknown",
        Received: row.created || "",
      }),
    });
    const body = await r.json().catch(() => ({}));
    return {
      ok: r.ok && String(body.success) === "true",
      status: r.status,
      detail: JSON.stringify(body).slice(0, 160),
    };
  } catch (e) {
    return { ok: false, status: 0, detail: String((e && e.message) || e).slice(0, 160) };
  }
}

async function viaResend(env, to, row) {
  const text = pairs(row).map(([k, v]) => `${k}: ${v}`).join("\n");
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
