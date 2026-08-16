# КАРТА ИСТОЧНИКОВ ЛИДОВ ПО РЫНКАМ (для базы ~3000)
Обновлено 14.08.2026 после проверки открытых данных.

## FLORIDA (пермиты дают контрактора + телефон) ✅
- **Miami-Dade** — ArcGIS `miamidade_permit_data`: ContractorName + Phone + объект + сумма. РАБОТАЕТ
  (текущая база 90+ целей). Дозагрузка по расписанию.
- **Broward** — портал BrOWD/EPermits; проверить наличие open-data с контрактором (след. шаг).
- **Palm Beach** — PBC ePZB / open data; проверить (след. шаг).
- Ожидаемый охват FL: ~1,200–1,800 целей (GC/owners с активными объектами).

## CALIFORNIA — пермиты БЕЗ контактов ❌ → источник = CSLB License Master ✅
Проверено: пермиты LA (data.lacity.org) и SF (data.sfgov.org) НЕ содержат контрактора/телефона;
реестр бизнесов SF — только название+адрес. Поэтому CA-лиды берём из:
- **CSLB Public Data Portal → License Master** (cslb.ca.gov/onlineservices/dataportal/ContractorList):
  бесплатно, поля: business name, **address, TELEPHONE**, license #, status, **classification(s)**,
  county, bond, WC. Фильтр под нас:
  - **County = Los Angeles + San Francisco (+ San Mateo/Alameda для Bay Area).**
  - **Классы-цели:**
    • **B (General Building)** и крупные C — как ПОКУПАТЕЛИ нашей поставки/site-services + возможные партнёры.
    • **C-35 (Plastering), C-15 (Flooring), C-54 (Tile), C-9 (Drywall), C-33 (Painting)** — потенциальные
      ПАРТНЁРЫ (RME/JV) для отделки под их лицензией.
  - Только status = Active. Дедуп по номеру лицензии/бизнесу.
  - Файл большой (statewide) — качаем и фильтруем офлайн; телефон есть → сразу очередь «звонок»
    (человек) + email-дискавери по названию для писем.
- Ожидаемый охват CA после фильтра: ~1,000–1,500 целевых лицензий (LA+SF+Bay).

## СЕГМЕНТАЦИЯ БАЗЫ (единый recipients-формат)
Поля: company, market (MDC/BROWARD/PBC/LA/SF), source (permit/cslb), trade_fit, license_class,
address, phone, email(если найден), project(если из пермита), status.
Правила по рынку (из licensing-roadmap): FL — отделка self-perform; CA — site services/supply
self-perform, отделка = supply/partner. Шаблоны писем разные (FL-finish / CA-services / supply / partner).

## ИТОГ ПО ОХВАТУ
FL ~1.2–1.8k + CA ~1.0–1.5k = **~2.5–3.3k целей** → цель ~3000 достижима.
Темп рассылки — 25–40 email/день на домен (deliverability), CA-телефоны → очередь звонков,
warm → Twilio SMS. Мгновенно не заливаем.

## СЛЕДУЮЩИЕ ШАГИ (я делаю)
1. CSLB License Master → фильтр LA+SF+классы → CA-база с телефонами.
2. Broward + Palm Beach пермиты → расширение FL-базы.
3. Единый recipients с сегментами + шаблоны по рынку/услуге.
4. (после Twilio-кредов) — warm-SMS модуль.
