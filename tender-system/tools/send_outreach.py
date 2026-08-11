#!/usr/bin/env python3
"""
Отправка коммерческого outreach по recipients.csv через SMTP.

Секреты — ТОЛЬКО из переменных окружения (в репозитории не хранятся):
  SMTP_HOST  (default: smtp.gmail.com)
  SMTP_PORT  (default: 587)
  SMTP_USER  (адрес отправителя, напр. info@ispgroupgc.com)
  SMTP_PASS  (app password)

Правила:
  - дневной лимит (--limit, default 30) — защита от спам-фильтров
  - шлёт только строки со статусом DRAFT_READY_TO_SEND и заполненным email
  - после отправки: status=SENT_<дата>, лог в sent-log.csv
  - CAN-SPAM: физический адрес в подписи + строка opt-out добавляется автоматически
  - --dry-run: показать, что будет отправлено, без отправки
  - --test you@example.com: одно тестовое письмо себе

Запуск: python3 send_outreach.py [--limit 30] [--dry-run] [--test EMAIL]
"""
import csv, os, smtplib, ssl, sys, time, datetime
from email.mime.text import MIMEText
from email.utils import formataddr

BASE = os.path.join(os.path.dirname(__file__), "..", "outreach", "mdc-2026-08")
CSV_PATH = os.path.join(BASE, "recipients.csv")
LOG_PATH = os.path.join(BASE, "sent-log.csv")

FOOTER = (
    "\n\n--\n"
    "ISP GROUP LLC, 16395 Biscayne Blvd Apt 818, Aventura, FL 33160\n"
    "If you'd prefer not to receive supplier introductions from us, reply with \"remove\" and we won't email again.\n"
)

def send_batch(limit=30, dry=False, test=None):
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    pw = os.environ.get("SMTP_PASS")
    if not (user and pw) and not dry:
        sys.exit("SMTP_USER/SMTP_PASS не заданы в окружении. См. настройку в PLAYBOOK.")

    def deliver(to_addr, subject, body):
        msg = MIMEText(body + FOOTER, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = formataddr(("Aleksandr Orlov, ISP GROUP LLC", user))
        msg["To"] = to_addr
        msg["Reply-To"] = user
        with smtplib.SMTP(host, port, timeout=60) as s:
            s.starttls(context=ssl.create_default_context())
            s.login(user, pw)
            s.sendmail(user, [to_addr], msg.as_string())

    if test:
        deliver(test, "ISP GROUP outreach — тест отправки", "Тест SMTP-отправки. Если вы это видите — канал работает.")
        print("test sent ->", test); return

    rows = list(csv.DictReader(open(CSV_PATH)))
    sent = 0
    today = datetime.date.today().isoformat()
    for r in rows:
        if sent >= limit: break
        if r["status"] != "DRAFT_READY_TO_SEND" or "@" not in r.get("email", ""):
            continue
        body = open(os.path.join(os.path.dirname(CSV_PATH), "..", "..", r["letter_file"])
                    if not os.path.isabs(r["letter_file"]) else r["letter_file"]).read()
        # первая строка письма-файла — "Subject: ..."; отделяем
        lines = body.split("\n")
        subject = lines[0].replace("Subject:", "").strip()
        text = "\n".join(lines[1:]).strip()
        if dry:
            print(f"[DRY] {r['email']:40} | {subject[:70]}"); sent += 1; continue
        try:
            deliver(r["email"], subject, text)
            r["status"] = f"SENT_{today}"
            sent += 1
            with open(LOG_PATH, "a", newline="") as lf:
                csv.writer(lf).writerow([today, r["email"], r["contractor"], subject])
            print(f"sent {sent}: {r['email']}")
            time.sleep(45)  # анти-спам пауза между письмами
        except Exception as e:
            r["status"] = f"ERROR_{type(e).__name__}"
            print("ERROR", r["email"], repr(e)[:120])
    with open(CSV_PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("batch done, sent:", sent)

if __name__ == "__main__":
    args = sys.argv[1:]
    dry = "--dry-run" in args
    test = args[args.index("--test") + 1] if "--test" in args else None
    limit = int(args[args.index("--limit") + 1]) if "--limit" in args else 30
    send_batch(limit=limit, dry=dry, test=test)
