# Данные для копирования в регистрационные формы (бесплатная волна)

Единый блок значений для всех форм. Платные ресурсы отложены (решение 2026-08-10):
Texas CMBL, платные пакеты BidNet, подписка DemandStar — НЕ оформлять без отдельного разрешения.

## Company
| Поле формы | Значение |
|---|---|
| Legal / Company Name | ISP GROUP LLC |
| Entity Type | Limited Liability Company (LLC), tax classification S corporation |
| EIN / Federal Tax ID | 38-4380828 |
| UEI | WA46PAMTYMQ7 |
| CAGE | 217F4 |
| Address | 16395 Biscayne Blvd Apt 818 |
| City / State / ZIP | Aventura, FL 33160-5743 |
| Phone | (929) 707-5551 |
| Email | info@ispgroupgc.com |
| Contact | Aleksandr Orlov, Managing Member |

## Товарные коды (выбирать в профиле каждой площадки)
- **NIGP:** 750 (Road/Highway Building Materials: sand, gravel, crushed stone), 020 (Agricultural/Construction Equipment), 545 (Machinery & Heavy Hardware), 755, 760, 420 (Furniture, Office), 425 (Furniture, School/Institutional)
- **UNSPSC:** сегменты 11 (Minerals/Ores — aggregates), 30 (Structural Materials), 22 (Building/Construction Machinery), 56 (Furniture & Furnishings)
- **PSC:** 5610, 3805, 3810, 7105, 7110, 7125

### NAICS в карточке SAM, сверено 13.10.2026 по экрану Goods & Services

Прежняя запись «212319, 212321, 423810, 337127» была **неверной**, таких
кодов в карточке нет. Фактически компания заведена как строительный
подрядчик и сервисная служба, товарных кодов нет ни одного:

| NAICS | |
|---|---|
| 236118 | Residential Remodelers |
| **236220** | **Commercial and Institutional Building Construction, PRIMARY** |
| 238140 | Masonry Contractors |
| 238310 | Drywall and Insulation Contractors |
| 238320 | Painting and Wall Covering Contractors |
| 238350 | Finish Carpentry Contractors |
| 238390 | Other Building Finishing Contractors |
| 238910 | Site Preparation Contractors |
| 238990 | All Other Specialty Trade Contractors (исключения 1 и 2) |
| 561210 | Facilities Support Services |
| 561720 | Janitorial Services |
| 561730 | Landscaping Services |
| 561790 | Other Services to Buildings and Dwellings |
| 562910 | Remediation Services (исключения 1 и 2) |

Отсюда следует: по всем товарным закупкам, которые мы готовили, карточка
нас не покрывала. Что добавлять, см. `sourcing/kody-sam.md`. Строительные и
сервисные коды **не удалять**: они открывают уборку, озеленение и
обслуживание объектов, где закупки есть.

## Очередь бесплатных регистраций
1. **BidNet Direct** — bidnetdirect.com/registration → free-tier, группы FL/TX/CA/NY/NJ, NIGP-коды выше
2. **MyFloridaMarketPlace VIP** — vendor.myfloridamarketplace.com (перед этим: FL Substitute W-9 на flvendor.myfloridacfo.com — нужен подписанный W-9)
3. **TIPS** — tips.ionwave.net → commodities: Furniture; Heavy/Infrastructure Equipment; Trades/Materials
4. **NJSTART** — njstart.gov → NIGP-коды
5. **NYS Contract Reporter** — nyscr.ny.gov → категории материалов/техники/мебели
6. **Cal eProcure** — caleprocure.ca.gov → UNSPSC, Receive Notification = Yes
7. **BuyBoard** — buyboard.com vendor registration
8. **DemandStar** — network.demandstar.com → free-tier, 1 агентство FL (рекомендация: St. Lucie County)
9. **ESBD (Texas)** — без регистрации: мониторинг txsmartbuy.gov/esbd (CMBL отложен — платный)

На каждом шаге: пароли создавать в менеджере паролей (в git не хранить), email-верификация придёт на info@ispgroupgc.com, финальное принятие Terms — вручную пользователем.
