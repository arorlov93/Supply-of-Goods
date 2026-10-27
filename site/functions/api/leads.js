/* Заявки: чтение и изменение статуса. Адрес /api/leads.
 *
 * Доступ по общему паролю из переменной CRM_SECRET, заданной в настройках
 * проекта Pages. Пароля в репозитории нет и быть не должно. Браузер шлёт
 * его заголовком X-CRM-Key, страница /crm хранит его только в памяти
 * вкладки, то есть он исчезает вместе с ней.
 *
 * Сравнение пароля идёт по всей длине без ранних выходов: обычное
 * сравнение строк завершается на первом несовпавшем знаке, и по времени
 * ответа пароль можно подбирать по буквам.
 */

const STATUSES = ["new", "qualified", "quoted", "won", "lost"];
const COLS = "id,created,name,mail,co,country,cat,terms,qty,dest,spec,page,ip_country,status,note,updated";

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
}

function sameSecret(given, expected) {
  if (!expected) return false;
  const a = new TextEncoder().encode(String(given || ""));
  const b = new TextEncoder().encode(expected);
  let diff = a.length ^ b.length;
  for (let i = 0; i < Math.max(a.length, b.length); i++) diff |= (a[i] || 0) ^ (b[i] || 0);
  return diff === 0;
}

function guard(ctx) {
  if (!ctx.env.CRM_SECRET) return json({ ok: false, code: "not_configured" }, 503);
  const key = ctx.request.headers.get("x-crm-key");
  if (!sameSecret(key, ctx.env.CRM_SECRET)) return json({ ok: false, code: "forbidden" }, 403);
  if (!ctx.env.DB) return json({ ok: false, code: "no_database" }, 503);
  return null;
}

export async function onRequestGet(ctx) {
  const stop = guard(ctx);
  if (stop) return stop;
  const url = new URL(ctx.request.url);
  const status = url.searchParams.get("status");
  try {
    const q = status && STATUSES.includes(status)
      ? ctx.env.DB.prepare(`SELECT ${COLS} FROM leads WHERE status = ? ORDER BY created DESC LIMIT 500`).bind(status)
      : ctx.env.DB.prepare(`SELECT ${COLS} FROM leads ORDER BY created DESC LIMIT 500`);
    const { results } = await q.all();
    const counts = await ctx.env.DB
      .prepare("SELECT status, COUNT(*) AS n FROM leads GROUP BY status").all();
    return json({ ok: true, leads: results || [], counts: counts.results || [] });
  } catch (e) {
    console.log("leads read failed", String(e && e.message || e).slice(0, 200));
    return json({ ok: false, code: "db_error" }, 500);
  }
}

export async function onRequestPost(ctx) {
  const stop = guard(ctx);
  if (stop) return stop;
  let d;
  try { d = await ctx.request.json(); } catch { return json({ ok: false, code: "bad_json" }, 400); }

  const id = parseInt(d.id, 10);
  if (!Number.isInteger(id) || id < 1) return json({ ok: false, code: "bad_id" }, 400);
  if (d.status != null && !STATUSES.includes(d.status)) return json({ ok: false, code: "bad_status" }, 400);
  if (d.note != null && String(d.note).length > 4000) return json({ ok: false, code: "too_long" }, 400);

  try {
    if (d.status != null) {
      await ctx.env.DB.prepare("UPDATE leads SET status = ?, updated = ? WHERE id = ?")
        .bind(d.status, new Date().toISOString(), id).run();
    }
    if (d.note != null) {
      await ctx.env.DB.prepare("UPDATE leads SET note = ?, updated = ? WHERE id = ?")
        .bind(String(d.note), new Date().toISOString(), id).run();
    }
    return json({ ok: true });
  } catch (e) {
    console.log("leads write failed", String(e && e.message || e).slice(0, 200));
    return json({ ok: false, code: "db_error" }, 500);
  }
}
