# PIPELINE C — PRIME CONTRACTORS SCAN (USASpending) — 10 августа 2026

**Источник:** USASpending API, новые федеральные контракты (new awards) за 2026-02-01 → 2026-08-10,
NAICS 2361/2362/2371/2373/2379/2383/2389/5612, place of performance FL/TX/CA/NY/NJ.

**Собрано:** 1000 awards → 507 активных (≥$300K, окончание после 2026-09) → **328 уникальных primes**, из них **103 со score ≥ 80**.

По штатам (primes): FL 76, TX 87, CA 110, NY 46, NJ 22.

**Score primes (0-100):** fit проекта под supply-профиль ISP (до 40: дороги/heavy civil выше зданий), объём портфеля (до 20, sweet spot $1M-$300M), свежесть старта (до 20: старт после мая 2026 = закупки идут сейчас), география (до 10), число контрактов (до 10).

**Стадия CRM:** все primes → `PRIME_FOUND`. Контакты procurement (email/phone) в USASpending отсутствуют — следующий шаг: contact search (SAM entity + сайты компаний), затем outreach-драфты (отправка только после одобрения пользователя, EMAIL_MODE=DRAFT).

## TOP-15 PRIMES OVERALL

| # | Prime | Score | Штаты | Awards | Объём | Ключевой контракт | Агентство | NAICS | Роль ISP | Ссылка |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CDEEM CO | **100** | NJ/NY | 4 | $81.0M | THE GENERAL CONTRACTOR SHALL PROVIDE ALL LABOR, MATERIALS, EQUIPMENT, … ($39.5M, до 2028-07-13) | Department of Veterans Affairs | 236220 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_36C77626C0069_3600_-NONE-_-NONE-) |
| 2 | CURTIN MARITIME CORP | **96** | CA/FL | 2 | $13.9M | U.S NAVAL STATION MAYPORT MAINTENANCE DREDGING, DUVAL COUNTY, FLORIDA… ($9.0M, до 2026-11-24) | Department of the Army | 237990 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_W912EP26CA014_9700_-NONE-_-NONE-) |
| 3 | MCNEAL PROFESSIONAL SERVICES, INC. | **96** | FL/TX | 2 | $2.6M | BPT RCAG TOWERS AND BUILDINGS REPLACEMENT @ LUFKIN (LFK), TX.… ($1.7M, до 2027-01-06) | Federal Aviation Administratio | 237130 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_6973GH26C00155_6920_-NONE-_-NONE-) |
| 4 | US DIVERSIFIED CONTRACTING SERVICES INC. | **96** | FL/NY | 2 | $1.1M | INSTALLATION OF EMERGENCY GENERATOR AT CALVERTON NATL CEMETERY NCA'S N… ($842K, до 2027-01-08) | Department of Veterans Affairs | 236220 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_36C78626N0350_3600_36C78625D0038_3600) |
| 5 | ANNA LISA LUNA CONSTRUCTION, INC. | **95** | CA | 4 | $18.5M | WRMACC SEED POOL 2, REPAIR TAXIWAY PHASE 1… ($7.2M, до 2028-03-12) | National Aeronautics and Space | 236220 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_80AFRC26FA047_8000_80AFRC26DA004_8000) |
| 6 | JUDD BUICK CONSTRUCTION, INC. | **95** | CA | 5 | $14.5M | 03 - CON - ARA, ROAD REPAIRS… ($4.0M, до 2027-11-30) | Forest Service | 237310 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_12363N26F4102_12C2_12363N23A4239_12C2) |
| 7 | MAVERICK CONSTRUCTORS, LLC | **95** | FL/TX | 3 | $9.8M | IN ACCORDANCE WITH FAR 36.204(G), DISCLOSURE OF THE MAGNITUDE OF CONST… ($4.0M, до 2027-06-08) | Department of the Army | 237990 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_W912HY26CA011_9700_-NONE-_-NONE-) |
| 8 | ALEUT CONSTRUCTION LLC | **95** | FL | 8 | $8.3M | UPGRADE MECHANICAL AND COMPRESSED AIR SYSTEMS PAYLOAD HAZARD SERVICING… ($2.9M, до 2027-01-22) | National Aeronautics and Space | 236220 | техника, материалы, суб-без-лицензии, site services | [award](https://www.usaspending.gov/award/CONT_AWD_80KSC026FA031_8000_80KSC021DA005_8000) |
| 9 | CROWN INNOVATIONS, INC. | **95** | CA | 4 | $3.1M | OES- UIS, THE PURPOSE OF THIS MODIFICATION IS TO FUND UIS FLOATING CRE… ($1.1M, до 2027-02-12) | Federal Aviation Administratio | 237130 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_693KA826F00181_6920_693KA825D00004_6920) |
| 10 | RANCO CONSTRUCTION INC | **95** | NJ | 4 | $1.7M | INSTALL SECURITY FENCES AT RANGE WATER WELLS HEKP 19-1021… ($538K, до 2027-03-05) | Department of the Air Force | 237310 | техника, материалы, суб-без-лицензии, site services | [award](https://www.usaspending.gov/award/CONT_AWD_FA448426F0142_9700_FA448425D0013_9700) |
| 11 | SOUTH DADE AIR CONDITIONING & REFRIGERATION INC | **94** | NY | 3 | $5.6M | COMPLETE FACILITIES MAINTENANCE AT THE ALEXANDER HAMILTON U.S. CUSTOM … ($4.6M, до 2027-06-30) | Public Buildings Service | 561210 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_47PF5226F0009_4740_47PC0621A0002_4740) |
| 12 | RG TENNEY ELECTRIC INC | **94** | FL | 3 | $5.2M | LAKE CITY, FL - QJY RCAG FULL SITE REPLACEMENT IN LAKE CITY, FL IN ACC… ($2.7M, до 2027-12-31) | Federal Aviation Administratio | 237130 | техника, материалы | [award](https://www.usaspending.gov/award/CONT_AWD_6973GH26C00154_6920_-NONE-_-NONE-) |
| 13 | WHITE BEAR CONSTRUCTION, INC. | **94** | CA | 3 | $2.1M | 127EAW26P0017 - GAOA, LASSEN FOREST-WIDE TOILET REPLACEMENT… ($784K, до 2026-10-30) | Forest Service | 237990 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_127EAW26P0017_12C2_-NONE-_-NONE-) |
| 14 | WEEKS MARINE, INC. | **92** | FL/TX | 2 | $94.0M | FY26 REDFISH TO MORGANS, HOPPER DREDGING… ($66.5M, до 2027-05-21) | Department of the Army | 237990 | техника, материалы | [award](https://www.usaspending.gov/award/CONT_AWD_W912HY26CA016_9700_-NONE-_-NONE-) |
| 15 | DEAN MARINE AND EXCAVATING, INC. | **91** | NY | 2 | $25.2M | OSWEGO BREAKWATER WORK… ($14.9M, до 2027-12-05) | Department of the Army | 237990 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_W912P426CA009_9700_-NONE-_-NONE-) |

## ДОРОГИ / HEAVY CIVIL (ядро для щебня и заполнителей)

Primes с ключевым контрактом NAICS 2371/2373/2379 — целевые покупатели aggregate, road base, riprap, песка, бетона и аренды/поставки техники.

| # | Prime | Score | Штаты | Awards | Объём | Ключевой контракт | Агентство | NAICS | Роль ISP | Ссылка |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CURTIN MARITIME CORP | **96** | CA/FL | 2 | $13.9M | U.S NAVAL STATION MAYPORT MAINTENANCE DREDGING, DUVAL COUNTY, FLORIDA… ($9.0M, до 2026-11-24) | Department of the Army | 237990 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_W912EP26CA014_9700_-NONE-_-NONE-) |
| 2 | MCNEAL PROFESSIONAL SERVICES, INC. | **96** | FL/TX | 2 | $2.6M | BPT RCAG TOWERS AND BUILDINGS REPLACEMENT @ LUFKIN (LFK), TX.… ($1.7M, до 2027-01-06) | Federal Aviation Administratio | 237130 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_6973GH26C00155_6920_-NONE-_-NONE-) |
| 3 | JUDD BUICK CONSTRUCTION, INC. | **95** | CA | 5 | $14.5M | 03 - CON - ARA, ROAD REPAIRS… ($4.0M, до 2027-11-30) | Forest Service | 237310 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_12363N26F4102_12C2_12363N23A4239_12C2) |
| 4 | MAVERICK CONSTRUCTORS, LLC | **95** | FL/TX | 3 | $9.8M | IN ACCORDANCE WITH FAR 36.204(G), DISCLOSURE OF THE MAGNITUDE OF CONST… ($4.0M, до 2027-06-08) | Department of the Army | 237990 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_W912HY26CA011_9700_-NONE-_-NONE-) |
| 5 | CROWN INNOVATIONS, INC. | **95** | CA | 4 | $3.1M | OES- UIS, THE PURPOSE OF THIS MODIFICATION IS TO FUND UIS FLOATING CRE… ($1.1M, до 2027-02-12) | Federal Aviation Administratio | 237130 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_693KA826F00181_6920_693KA825D00004_6920) |
| 6 | RANCO CONSTRUCTION INC | **95** | NJ | 4 | $1.7M | INSTALL SECURITY FENCES AT RANGE WATER WELLS HEKP 19-1021… ($538K, до 2027-03-05) | Department of the Air Force | 237310 | техника, материалы, суб-без-лицензии, site services | [award](https://www.usaspending.gov/award/CONT_AWD_FA448426F0142_9700_FA448425D0013_9700) |
| 7 | RG TENNEY ELECTRIC INC | **94** | FL | 3 | $5.2M | LAKE CITY, FL - QJY RCAG FULL SITE REPLACEMENT IN LAKE CITY, FL IN ACC… ($2.7M, до 2027-12-31) | Federal Aviation Administratio | 237130 | техника, материалы | [award](https://www.usaspending.gov/award/CONT_AWD_6973GH26C00154_6920_-NONE-_-NONE-) |
| 8 | WHITE BEAR CONSTRUCTION, INC. | **94** | CA | 3 | $2.1M | 127EAW26P0017 - GAOA, LASSEN FOREST-WIDE TOILET REPLACEMENT… ($784K, до 2026-10-30) | Forest Service | 237990 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_127EAW26P0017_12C2_-NONE-_-NONE-) |
| 9 | WEEKS MARINE, INC. | **92** | FL/TX | 2 | $94.0M | FY26 REDFISH TO MORGANS, HOPPER DREDGING… ($66.5M, до 2027-05-21) | Department of the Army | 237990 | техника, материалы | [award](https://www.usaspending.gov/award/CONT_AWD_W912HY26CA016_9700_-NONE-_-NONE-) |
| 10 | DEAN MARINE AND EXCAVATING, INC. | **91** | NY | 2 | $25.2M | OSWEGO BREAKWATER WORK… ($14.9M, до 2027-12-05) | Department of the Army | 237990 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_W912P426CA009_9700_-NONE-_-NONE-) |
| 11 | TLI CONSTRUCTION, INC. | **91** | CA | 6 | $7.7M | RPR WEST FORBES AVENUE (NIGHTINGALE TO SOUTH ROSAMOND)… ($1.9M, до 2026-09-17) | Department of the Air Force | 237310 | техника, материалы, суб-без-лицензии, site services | [award](https://www.usaspending.gov/award/CONT_AWD_FA930126F0104_9700_FA930123D0005_9700) |
| 12 | SERVIAM CONSTRUCTION LLC | **91** | NY | 2 | $2.1M | 528A6-22-665 REBUILD B29A PARKING LOT… ($1.3M, до 2026-12-30) | Department of Veterans Affairs | 237310 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_36C24226C0092_3600_-NONE-_-NONE-) |

## ЗДАНИЯ (236x) — материалы, мебель, interior-субподряд, site cleanup

| # | Prime | Score | Штаты | Awards | Объём | Ключевой контракт | Агентство | NAICS | Роль ISP | Ссылка |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CDEEM CO | **100** | NJ/NY | 4 | $81.0M | THE GENERAL CONTRACTOR SHALL PROVIDE ALL LABOR, MATERIALS, EQUIPMENT, … ($39.5M, до 2028-07-13) | Department of Veterans Affairs | 236220 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_36C77626C0069_3600_-NONE-_-NONE-) |
| 2 | US DIVERSIFIED CONTRACTING SERVICES INC. | **96** | FL/NY | 2 | $1.1M | INSTALLATION OF EMERGENCY GENERATOR AT CALVERTON NATL CEMETERY NCA'S N… ($842K, до 2027-01-08) | Department of Veterans Affairs | 236220 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_36C78626N0350_3600_36C78625D0038_3600) |
| 3 | ANNA LISA LUNA CONSTRUCTION, INC. | **95** | CA | 4 | $18.5M | WRMACC SEED POOL 2, REPAIR TAXIWAY PHASE 1… ($7.2M, до 2028-03-12) | National Aeronautics and Space | 236220 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_80AFRC26FA047_8000_80AFRC26DA004_8000) |
| 4 | ALEUT CONSTRUCTION LLC | **95** | FL | 8 | $8.3M | UPGRADE MECHANICAL AND COMPRESSED AIR SYSTEMS PAYLOAD HAZARD SERVICING… ($2.9M, до 2027-01-22) | National Aeronautics and Space | 236220 | техника, материалы, суб-без-лицензии, site services | [award](https://www.usaspending.gov/award/CONT_AWD_80KSC026FA031_8000_80KSC021DA005_8000) |
| 5 | MCKENZIE CONSTRUCTION & SITE DEVELOPMENT LLC | **91** | TX | 2 | $13.8M | FY26-002698 APPROVED FY26-003873 APPROVED DISASTER RECOVERY - HEAVY MA… ($9.8M, до 2026-11-30) | Forest Service | 236220 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_12445126F0014_12C2_140F0822D0073_1448) |
| 6 | ROCK CONSTRUCTION MANAGEMENT LLC | **91** | TX | 2 | $6.4M | NRM UPGRADE UTILITY GRAND PRAIRIE… ($5.6M, до 2027-11-19) | Department of Veterans Affairs | 236220 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_36C25726C0047_3600_-NONE-_-NONE-) |
| 7 | ARMITAGE SAI JV | **90** | NY | 3 | $11.6M | EE-24009-4J, 2025 BRIDGE PAINTING CONTRACT… ($6.0M, до 2028-04-16) | Department of the Army | 236220 | техника, материалы, суб-без-лицензии, site services | [award](https://www.usaspending.gov/award/CONT_AWD_W911S226FA094_9700_W911S225DA025_9700) |
| 8 | IRON SWORD ENTERPRISES, LLC | **90** | NY | 3 | $7.8M | CASTLE POINT ROOFS… ($6.5M, до 2028-09-30) | Department of Veterans Affairs | 236220 | техника, материалы, суб-без-лицензии, site services | [award](https://www.usaspending.gov/award/CONT_AWD_36C24226C0061_3600_-NONE-_-NONE-) |
| 9 | EASTERN CONSTRUCTION & ELECTRIC INC | **90** | NJ | 3 | $4.2M | MACC TASK ORDER:  THE CONTRACTOR SHALL REPAIR ADMINISTRATIVE FACILITY,… ($2.5M, до 2026-09-03) | Department of the Air Force | 236220 | техника, материалы, суб-без-лицензии, site services | [award](https://www.usaspending.gov/award/CONT_AWD_FA448426F0085_9700_FA448425D0006_9700) |
| 10 | MILLER ELECTRIC COMPANY INC. | **87** | CA | 2 | $2.6M | FHL BLDG 228 POWERLINE AND POLE REPAIR AND REPLACEMENT… ($1.9M, до 2027-04-28) | Department of the Army | 236220 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_W911SA26FA144_9700_W911SA23D2014_9700) |

## SPECIALTY / FACILITY (2383/2389/5612)

| # | Prime | Score | Штаты | Awards | Объём | Ключевой контракт | Агентство | NAICS | Роль ISP | Ссылка |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SOUTH DADE AIR CONDITIONING & REFRIGERATION INC | **94** | NY | 3 | $5.6M | COMPLETE FACILITIES MAINTENANCE AT THE ALEXANDER HAMILTON U.S. CUSTOM … ($4.6M, до 2027-06-30) | Public Buildings Service | 561210 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_47PF5226F0009_4740_47PC0621A0002_4740) |
| 2 | J&J AND ALMS MISSION SUPPORT SOLUTIONS, LLC | **91** | FL | 5 | $11.1M | NASP BOSC OP3 FFP FUNDING TASK ORDER… ($8.1M, до 2027-03-31) | Department of the Navy | 561210 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_N6945026F0092_9700_N6945022D0043_9700) |
| 3 | SEDONA-NASCO JV2, LLC | **91** | TX | 14 | $4.9M | B1001 - REPLACE CAST IRON PIPE… ($498K, до 2026-12-27) | Department of the Army | 238990 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_W9126G26FA096_9700_W9126G23D0038_9700) |
| 4 | GSD SERVICES, LLC | **84** | CA | 1 | $2.9M | BOSC BRIDGEPORT CALIFORNIA - EXERCISE 2ND OPTION YEAR, MARINE CORPS MO… ($2.9M, до 2027-02-28) | Department of the Navy | 561210 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_N6247326F0170_9700_N6247323D3604_9700) |
| 5 | BEN FITZGERALD REAL ESTATE SERVICES, L.L.C. | **84** | CA | 1 | $1.7M | BRIDGE CONTRACT FOR A PERIOD OF PERFORMANCE FROM MARCH 1, 2026 TO JUNE… ($1.7M, до 2026-09-20) | U.S. Customs and Border Protec | 561210 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_70B01C26F00000160_7014_GS06Q17BQDS204_4732) |
| 6 | BACOPA SERVICES LLC | **80** | FL | 1 | $428K | CLEAN AND INSPECT CULVERTS - FLAMINGO… ($428K, до 2027-03-31) | National Park Service | 238990 | техника, материалы | [award](https://www.usaspending.gov/award/CONT_AWD_140P5426P0027_1443_-NONE-_-NONE-) |
| 7 | ACTION FACILITIES MANAGEMENT INC | **78** | NY/TX | 5 | $8.7M | BPA CALL 47PF5226F0010, COMPLETE FACILITIES MAINTENANCE SERVICES AT TH… ($4.5M, до 2027-06-30) | Public Buildings Service | 561210 | материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_47PF5226F0010_4740_47PC0621A0001_4740) |
| 8 | RASCAP LLC | **76** | NY | 1 | $319K | INSPECT & REPAIR FIRE DAMPERS… ($319K, до 2031-03-31) | Department of Veterans Affairs | 238990 | техника, материалы, site services | [award](https://www.usaspending.gov/award/CONT_AWD_36C24226C0070_3600_-NONE-_-NONE-) |

## Следующие шаги (Pipeline C)

1. **CONTACT_FOUND:** по TOP-30 primes найти procurement/estimating контакты (сайт, SAM entity data, LinkedIn) — задача следующего цикла.
2. **OUTREACH:** подготовить драфты писем «material/equipment supplier introduction» по ролям (щебень для дорожных primes; мебель/материалы для building primes). Отправка — только после одобрения пользователя.
3. Полные данные: `discovery/usaspending-primes-2026-08-10.json` (328 primes, отсортированы по score).

*Оговорка: роли ISP определены эвристикой по NAICS/PSC/описанию контракта — перед outreach каждый prime проверяется вручную (профиль компании, реальная потребность в материалах).*
