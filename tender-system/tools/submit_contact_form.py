#!/usr/bin/env python3
"""
Отправка outreach-сообщения через контактную форму сайта компании (легальный канал
вместо холодных SMS: форма = опубликованное приглашение к контакту).

Поддержка: Gravity Forms, Contact Form 7. CAPTCHA не обходим: если форма
защищена (Turnstile/reCAPTCHA) — статус SKIPPED_CAPTCHA, цель для ручного касания.

Использование:
  python3 submit_contact_form.py <contact_page_url> <message_file.txt>
Выход: OK <детали> | SKIPPED_CAPTCHA | FAIL <причина>
"""
import re, sys, requests

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36"}
IDENT = {
    "name": "Aleksandr Orlov", "first": "Aleksandr", "last": "Orlov",
    "email": "info@ispgroupgc.com", "phone": "(929) 707-5551",
    "company": "ISP GROUP LLC", "subject": "Subcontractor / supplier introduction — ISP GROUP LLC",
}

def classify(nm, label=""):
    t = (nm + " " + label).lower()
    if re.search(r'e-?mail', t): return "email"
    if re.search(r'phone|tel', t): return "phone"
    if re.search(r'first', t): return "first"
    if re.search(r'last|surname', t): return "last"
    if re.search(r'company|business', t): return "company"
    if re.search(r'subject', t): return "subject"
    if re.search(r'name', t): return "name"
    if re.search(r'message|comment|inquiry|question|describe|details|textarea', t): return "message"
    return None

def submit(url, message):
    s = requests.Session(); s.headers.update(UA)
    r = s.get(url, timeout=60); html = r.text
    if re.search(r'turnstile|g-recaptcha|h-captcha|recaptcha/api', html, re.I):
        # капча может быть и невидимой — но если объявлена в разметке формы, не пытаемся
        pass  # решаем по результату POST
    # ── Contact Form 7 ──
    m = re.search(r'action="[^"]*#(wpcf7-f(\d+)-[^"]*)"', html)
    if m and "wpcf7" in html:
        form = re.search(r'<form[^>]*wpcf7[^>]*>(.*?)</form>', html, re.S)
        body = form.group(1) if form else html
        data = {}
        for h in re.finditer(r'<input[^>]*type="hidden"[^>]*name="([^"]+)"[^>]*value="([^"]*)"', body):
            data[h.group(1)] = h.group(2)
        for inp in re.finditer(r'<(input|textarea)[^>]*name="([^"]+)"[^>]*>', body):
            nm = inp.group(2)
            if nm.startswith("_wpcf7") or nm in data: continue
            role = classify(nm) or ("message" if inp.group(1) == "textarea" else None)
            if role == "message": data[nm] = message
            elif role in IDENT: data[nm] = IDENT[role]
        resp = s.post(url, data=data, timeout=60, headers={"Referer": url})
        if re.search(r'mail_sent|wpcf7-mail-sent-ok|Thank you', resp.text, re.I): return "OK cf7"
        if re.search(r'captcha', resp.text, re.I): return "SKIPPED_CAPTCHA"
        return "FAIL cf7-unconfirmed"
    # ── Gravity Forms ──
    g = re.search(r"id='gform_(\d+)'", html) or re.search(r'id="gform_(\d+)"', html)
    if g:
        q = "'" if "id='gform_" in html else '"'
        fid = g.group(1)
        data = {}
        for h in re.finditer(rf"<input[^>]*type={q}hidden{q}[^>]*>", html):
            n = re.search(rf"name={q}([^{q}]*){q}", h.group(0)); v = re.search(rf"value={q}([^{q}]*){q}", h.group(0))
            if n: data[n.group(1)] = v.group(1) if v else ""
        # видимые поля с label
        labels = dict(re.findall(rf"<label[^>]*for={q}(input_[\d_]+){q}[^>]*>(.*?)</label>", html, re.S))
        for inp in re.finditer(rf"<(input|textarea)[^>]*id={q}(input_{fid}_[\d_]+){q}[^>]*>", html):
            iid = inp.group(2)
            nm = re.search(rf"name={q}([^{q}]+){q}", inp.group(0))
            if not nm: continue
            label = re.sub(r'<[^>]+>', '', labels.get(iid, ''))
            role = classify(nm.group(1) + " " + iid, label) or ("message" if inp.group(1) == "textarea" else None)
            if role == "message": data[nm.group(1)] = message
            elif role in IDENT: data[nm.group(1)] = IDENT[role]
        resp = s.post(url, data=data, timeout=60, headers={"Referer": url})
        if re.search(r'gform_confirmation_message', resp.text): return "OK gravity"
        if re.search(r'[Cc]aptcha|turnstile', resp.text): return "SKIPPED_CAPTCHA"
        return "FAIL gravity-unconfirmed"
    return "FAIL no-known-form"

if __name__ == "__main__":
    url, msg_file = sys.argv[1], sys.argv[2]
    print(submit(url, open(msg_file).read()))
