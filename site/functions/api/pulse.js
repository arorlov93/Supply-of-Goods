/* Пульс очереди заявок. Адрес /api/pulse.
 *
 * Зачем нужен отдельный адрес, когда есть /api/leads. Тот отдаёт сами
 * заявки и закрыт паролем CRM, который живёт только в настройках Pages и
 * в голове владельца. Здесь нужен не доступ к заявкам, а ответ на один
 * вопрос: есть ли заявки, о которых никому не сказали, и сколько они уже
 * лежат. По этому ответу внешняя проверка может поднять тревогу, ни
 * строчки переписки при этом не читая.
 *
 * Поэтому отдаётся только арифметика: сколько заявок без уведомления и
 * возраст самой старой из них в минутах. Ни имени, ни почты, ни текста
 * запроса здесь нет и быть не должно.
 *
 * Про ключ. Поставить его сюда я мог: токен Cloudflare умеет менять
 * переменные проекта Pages. Но рядом в тех же переменных лежит
 * CRM_SECRET типа secret_text, его значения не видит никто, включая
 * меня, и восстановить его в случае чего было бы нечем. Платить риском
 * сломать вход в CRM за сокрытие одного счётчика неразумно.
 *
 * Поэтому иначе: наружу отдаётся минимум, по которому нечего узнать.
 * Есть ли заявки без уведомления и сколько минут лежит самая старая.
 * Ни общего числа заявок, ни числа новых, то есть ни одного показателя
 * оборота. Если PULSE_KEY в переменных всё-таки появится, проверка
 * ключа включится сама, менять код не придётся.
 */

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

export async function onRequestGet(ctx) {
  const { env, request } = ctx;
  // ключ необязателен: если он задан, то обязателен
  if (env.PULSE_KEY && !sameSecret(request.headers.get("x-pulse-key"), env.PULSE_KEY)) {
    return json({ ok: false, code: "forbidden" }, 403);
  }
  if (!env.DB) return json({ ok: false, code: "no_database" }, 503);

  try {
    /* Колонку mailed заводит очередь, на старой базе её может не быть.
       Поэтому запрос с ней идёт первым, а без неё запасным: иначе
       проверка начнёт показывать отказ там, где всё в порядке. */
    let row;
    try {
      ({ results: [row] } = await env.DB.prepare(
        `SELECT COUNT(*) AS total,
                SUM(CASE WHEN COALESCE(mailed,0) = 0 THEN 1 ELSE 0 END) AS unsent,
                MIN(CASE WHEN COALESCE(mailed,0) = 0 THEN created END) AS oldest,
                SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) AS fresh
           FROM leads`
      ).all());
    } catch {
      ({ results: [row] } = await env.DB.prepare(
        `SELECT COUNT(*) AS total, 0 AS unsent, NULL AS oldest,
                SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) AS fresh
           FROM leads`
      ).all());
    }

    const oldest = row && row.oldest ? Date.parse(row.oldest) : null;
    return json({
      ok: true,
      unsent: (row && row.unsent) || 0,
      oldest_minutes: oldest ? Math.round((Date.now() - oldest) / 60000) : null,
      now: new Date().toISOString(),
    });
  } catch (e) {
    console.log("pulse failed", String((e && e.message) || e).slice(0, 200));
    return json({ ok: false, code: "db_error" }, 500);
  }
}
