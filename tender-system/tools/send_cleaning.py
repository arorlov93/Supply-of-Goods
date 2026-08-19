#!/usr/bin/env python3
"""
Универсальный клининг-отправитель. Работает по любой кампании-папке:
  <dir>/recipients.csv  (колонки: #,company,city,email,...,status; опц. project)
  <dir>/letter.txt      (шаблон; Subject: в 1-й строке; плейсхолдеры {company}, {project})

Шлёт статус DRAFT_READY_TO_SEND с валидным email → SENT_<дата>, лог в <dir>/sent-log.csv.
Brevo HTTPS API (ключ из .env). CAN-SPAM футер. --limit, --dry-run.

Запуск: python3 send_cleaning.py --dir tender-system/outreach/pm-2026-08 [--limit 25] [--dry-run]
"""
import csv, os, sys, time, datetime, json, urllib.request

_env = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
if os.path.exists(_env):
    for _l in open(_env):
        _l = _l.strip()
        if _l and "=" in _l and not _l.startswith("#"):
            k, v = _l.split("=", 1); os.environ.setdefault(k, v)

FOOTER = (
    "\n\n--\n"
    "ISP GROUP LLC, 16395 Biscayne Blvd Apt 818, Aventura, FL 33160\n"
    "If you'd prefer not to receive these introductions from us, reply with \"remove\" and we won't email again.\n"
)

def titlecase(name):
    small = {"and", "of", "the", "&"}
    return " ".join(w if (w.isupper() and len(w) <= 3) or w.lower() in small else w.capitalize()
                    for w in (name or "").strip().split())

def deliver(key, sender, to_addr, subject, body):
    payload = {"sender": {"name": "Aleksandr Orlov, ISP GROUP LLC", "email": sender},
               "to": [{"email": to_addr}], "bcc": [{"email": sender}],
               "replyTo": {"email": sender}, "subject": subject, "textContent": body + FOOTER}
    req = urllib.request.Request("https://api.brevo.com/v3/smtp/email",
        json.dumps(payload).encode(), {"api-key": key, "Content-Type": "application/json"})
    r = urllib.request.urlopen(req, timeout=60)
    if r.status not in (200, 201): raise RuntimeError(f"brevo {r.status}")

def send_batch(directory, limit=25, dry=False):
    key = os.environ.get("BREVO_API_KEY")
    sender = os.environ.get("SMTP_USER", "info@ispgroupgc.com")
    if not key and not dry: sys.exit("Нет BREVO_API_KEY в .env")
    csv_path = os.path.join(directory, "recipients.csv")
    tpl = open(os.path.join(directory, "letter.txt")).read().split("\n")
    subject_tpl = tpl[0].replace("Subject:", "").strip()
    body_tpl = "\n".join(tpl[1:]).strip()
    log_path = os.path.join(directory, "sent-log.csv")

    rows = list(csv.DictReader(open(csv_path)))
    sent = 0; today = datetime.date.today().isoformat()
    for r in rows:
        if sent >= limit: break
        if r.get("status") != "DRAFT_READY_TO_SEND" or "@" not in r.get("email", ""): continue
        company = titlecase(r.get("company", ""))
        subj = subject_tpl.replace("{company}", company).replace("{project}", r.get("project", ""))
        body = body_tpl.replace("{company}", company).replace("{project}", r.get("project", ""))
        if dry: print(f"[DRY] {r['email']:38} | {subj[:70]}"); sent += 1; continue
        try:
            deliver(key, sender, r["email"], subj, body)
            r["status"] = f"SENT_{today}"; sent += 1
            with open(log_path, "a", newline="") as lf:
                csv.writer(lf).writerow([today, r["email"], company, subj])
            print(f"sent {sent}: {r['email']}"); time.sleep(45)
        except Exception as e:
            r["status"] = f"ERROR_{type(e).__name__}"; print("ERROR", r["email"], repr(e)[:100])
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("cleaning batch done, sent:", sent)

if __name__ == "__main__":
    a = sys.argv[1:]
    d = a[a.index("--dir") + 1] if "--dir" in a else sys.exit("нужен --dir")
    dry = "--dry-run" in a
    limit = int(a[a.index("--limit") + 1]) if "--limit" in a else 25
    send_batch(d, limit=limit, dry=dry)
