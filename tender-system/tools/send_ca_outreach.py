#!/usr/bin/env python3
"""
Отправка CA (LA/SF/Bay) outreach по ca-2026-08/recipients.csv через Brevo HTTPS API.

CA recipients-формат: #,contractor,phone,city,market,classes,role,email,letter_template,status
Один общий шаблон letters/_template.txt с плейсхолдером {company} (Title Case из contractor).

Секреты — ТОЛЬКО из .env (gitignored): BREVO_API_KEY, SMTP_USER (отправитель).

Правила:
  - шлёт только строки со статусом DRAFT_READY_TO_SEND и валидным email
  - дневной лимит (--limit, default 20)
  - после отправки: status=SENT_<дата>, лог в sent-log.csv
  - CAN-SPAM: физ. адрес + opt-out в футере (добавляется автоматически)
  - --dry-run: показать без отправки

Запуск: python3 send_ca_outreach.py [--limit 20] [--dry-run]
"""
import csv, os, sys, time, datetime, json, urllib.request

_env = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
if os.path.exists(_env):
    for _l in open(_env):
        _l = _l.strip()
        if _l and "=" in _l and not _l.startswith("#"):
            k, v = _l.split("=", 1); os.environ.setdefault(k, v)

BASE = os.path.join(os.path.dirname(__file__), "..", "outreach", "ca-2026-08")
CSV_PATH = os.path.join(BASE, "recipients.csv")
LOG_PATH = os.path.join(BASE, "sent-log.csv")
TPL_PATH = os.path.join(BASE, "letters", "_template.txt")

FOOTER = (
    "\n\n--\n"
    "ISP GROUP LLC, 16395 Biscayne Blvd Apt 818, Aventura, FL 33160\n"
    "If you'd prefer not to receive supplier introductions from us, reply with \"remove\" and we won't email again.\n"
)

def titlecase(name):
    small = {"and", "of", "the", "&"}
    out = []
    for w in name.strip().split():
        out.append(w if (w.isupper() and len(w) <= 3) or w.lower() in small else w.capitalize())
    return " ".join(out)

def deliver(key, sender, to_addr, subject, body):
    payload = {
        "sender": {"name": "Aleksandr Orlov, ISP GROUP LLC", "email": sender},
        "to": [{"email": to_addr}],
        "bcc": [{"email": sender}],
        "replyTo": {"email": sender},
        "subject": subject,
        "textContent": body + FOOTER,
    }
    req = urllib.request.Request("https://api.brevo.com/v3/smtp/email",
        json.dumps(payload).encode(),
        {"api-key": key, "Content-Type": "application/json"})
    r = urllib.request.urlopen(req, timeout=60)
    if r.status not in (200, 201): raise RuntimeError(f"brevo {r.status}")

def send_batch(limit=20, dry=False):
    key = os.environ.get("BREVO_API_KEY")
    sender = os.environ.get("SMTP_USER", "info@ispgroupgc.com")
    if not key and not dry:
        sys.exit("Нет BREVO_API_KEY в .env")
    tpl = open(TPL_PATH).read().split("\n")
    subject_tpl = tpl[0].replace("Subject:", "").strip()
    body_tpl = "\n".join(tpl[1:]).strip()

    rows = list(csv.DictReader(open(CSV_PATH)))
    sent = 0
    today = datetime.date.today().isoformat()
    for r in rows:
        if sent >= limit: break
        if r["status"] != "DRAFT_READY_TO_SEND" or "@" not in r.get("email", ""):
            continue
        company = titlecase(r["contractor"])
        body = body_tpl.replace("{company}", company)
        if dry:
            print(f"[DRY] {r['email']:40} | {company}"); sent += 1; continue
        try:
            deliver(key, sender, r["email"], subject_tpl, body)
            r["status"] = f"SENT_{today}"
            sent += 1
            with open(LOG_PATH, "a", newline="") as lf:
                csv.writer(lf).writerow([today, r["email"], r["contractor"], subject_tpl])
            print(f"sent {sent}: {r['email']}")
            time.sleep(45)
        except Exception as e:
            r["status"] = f"ERROR_{type(e).__name__}"
            print("ERROR", r["email"], repr(e)[:120])
    with open(CSV_PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("CA batch done, sent:", sent)

if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "--dry-run" in args
    limit = int(args[args.index("--limit") + 1]) if "--limit" in args else 20
    send_batch(limit=limit, dry=dry)
