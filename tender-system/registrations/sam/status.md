# SAM.gov — СТАТУС: ✅ ЗАРЕГИСТРИРОВАН (Active)

- Login URL: https://sam.gov (вход через Login.gov)
- Entity: **ISP GROUP LLC** — Active Registration, Purpose: All Awards
- UEI: **WA46PAMTYMQ7** | CAGE: **217F4**
- Адрес: 16395 Biscayne Blvd Apt 818, Aventura, FL 33160-5743
- Expiration: **2027-07-28** (напоминание о продлении поставить на июнь 2027)

## Что осталось активировать (не требует новой регистрации)

- [x] Entity status = Active, дата продления зафиксирована (28.07.2027).
- [ ] Проверить NAICS-коды в профиле: 212319, 212321, 423810, 337127 (+ PSC 5610/3805/3810/7105/7110/7125).
- [ ] Проверить SBA size standard по этим NAICS → отметка Small Business (открывает set-aside тендеры на щебень).
- [ ] Создать saved searches / follow в Contract Opportunities: NAICS 212321 + PSC 5610 (штаты FL/TX/CA/NY/NJ), NAICS 423810, NAICS 337127.
- [ ] Сгенерировать **API key** (Account Details → Public API Key) для Get Opportunities API → сохранить ТОЛЬКО в `.env` как `SAM_API_KEY` (в репозиторий не коммитить).
- [ ] Записать UEI и CAGE в company-profile.yaml — они нужны для DIBBS/Unison и федеральных бидов.

## Данные, которые нужны от пользователя
- UEI, CAGE, дата продления SAM, подтверждение размера компании (сотрудники/выручка).
