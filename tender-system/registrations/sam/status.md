# SAM.gov — СТАТУС: ✅ ЗАРЕГИСТРИРОВАН

- Login URL: https://sam.gov (вход через Login.gov)
- Registration status: **registered** (подтверждено пользователем 2026-08-10)

## Что осталось активировать (не требует новой регистрации)

- [ ] Проверить, что entity status = Active, и зафиксировать дату ежегодного продления (`sam_renewal_date` в company-profile.yaml) — просроченный SAM блокирует awards.
- [ ] Проверить NAICS-коды в профиле: 212319, 212321, 423810, 337127 (+ PSC 5610/3805/3810/7105/7110/7125).
- [ ] Проверить SBA size standard по этим NAICS → отметка Small Business (открывает set-aside тендеры на щебень).
- [ ] Создать saved searches / follow в Contract Opportunities: NAICS 212321 + PSC 5610 (штаты FL/TX/CA/NY/NJ), NAICS 423810, NAICS 337127.
- [ ] Сгенерировать **API key** (Account Details → Public API Key) для Get Opportunities API → сохранить ТОЛЬКО в `.env` как `SAM_API_KEY` (в репозиторий не коммитить).
- [ ] Записать UEI и CAGE в company-profile.yaml — они нужны для DIBBS/Unison и федеральных бидов.

## Данные, которые нужны от пользователя
- UEI, CAGE, дата продления SAM, подтверждение размера компании (сотрудники/выручка).
