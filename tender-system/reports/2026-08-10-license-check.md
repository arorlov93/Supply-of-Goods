# LICENSE CHECK — TOP УСЛУГИ ИЗ SAM-СКАНА — 10 августа 2026

Проверены документы solicitation (скачаны с sam.gov, публичные attachments) для топ-кандидатов услуг из скана 2026-08-10. Вердикты: `license-check/verdicts/*.yaml` (с источниками). Рескоринг: license_feasibility 8 (unclear) заменён на фактический (20 / 0).

## Результаты

| Solicitation | Объект | Штат | Вердикт | Score до → после | Результат |
|---|---|---|---|---|---|
| 1232SA26Q0977 | Grounds Maintenance, Kerrville (USDA ARS) | TX | **NO** license (SOW: только механическое edging, «NO chemical edging») | 66 → **78 (B)** | ✅ **QUALIFIED** — кандидат №1 на bid |
| 1232SA26Q1227 | Exterior Painting VSB, Wyndmoor (USDA ARS) | PA | **NO** license (SF-1442: bonds NO; PA не лицензирует коммерческую покраску) | 59 → **71 (B)** | ✅ **QUALIFIED** — кандидат №2 на bid |
| FA466126Q0079 | Repaint F-84F/RB-66B, Dyess AFB | TX | **NO** license, НО квалификационный барьер: CM с 10+ лет aircraft restoration | 65 → 77 | ⚠️ QUALIFIED по лицензии, **NO BID по квалификации** |
| 697DCK-26-R-00332 | Grounds Maintenance TRACON/ARTCC (FAA) | CA | **YES** — CA DPR licensed applicators (гербициды обязательны в SOW) | 66 → 58 | ❌ NO BID (лицензия применителя; score < 70 — без partner track) |
| 140P4226Q0048 | Historic Exterior Painting, INDE (NPS) | PA | **UNCLEAR** — lead paint removal: EPA/OSHA сертификации + hazwaste licensing | 59 → 59 | ❌ MANUAL REVIEW / NO PRIORITY (историч. реставрация — не наш профиль) |

## Поправка по eligibility (не license): set-aside фильтр

Из TOP УСЛУГИ исходного отчёта исключаются по set-aside (у ISP нет сертификаций 8(a)/SDVOSB):

- Palatka Custodial & Mowing (W912EP26QA006) — **8(a)** → NO BID
- NCRME Cleaning San Antonio (36C25726Q0795) — SDVOSBC → NO BID
- Janitorial El Paso (36C25726Q0659) — SDVOSBS → NO BID
- Landscape/Grounds Fresno (36C26126Q0750) — SDVOSBS → NO BID

**SBA (total small business) set-asides ISP проходит** — они остаются в работе.

## Действия

1. **1232SA26Q0977 (TX grounds, deadline 2026-08-28)** → Pipeline A: QUALIFIED → BID/NO BID. Нужны: расчёт трудозатрат по SOW (площади в A04 + карта AZ2), wage rates из C04c.
2. **1232SA26Q1227 (PA painting, deadline 2026-09-08)** → Pipeline A: QUALIFIED → BID/NO BID. Простой объём (CMU 40×55×14 ft, ~45 lf трещин): хорош как первый федеральный bid. Нужен субподрядчик-маляр или собственная бригада + расценка.
3. Dyess repaint — в архив с пометкой «качественный fit, но барьер опыта».
4. CA TRACON — вариант вернуться с licensed applicator субподрядчиком: только если пользователь захочет (низкий приоритет, score 58).

*Официальная подача бидов — только после одобрения пользователя (REQUIRE_HUMAN_APPROVAL).* 
