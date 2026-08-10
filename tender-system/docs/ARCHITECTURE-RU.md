# АРХИТЕКТУРА v2 — TENDER INTELLIGENCE & BID OPERATIONS SYSTEM (ISP GROUP)

**Обновлено:** 10 августа 2026 (директива пользователя)
**Заменяет:** односегментную supply-архитектуру v1

---

## ГЛАВНОЕ ПРАВИЛО СИСТЕМЫ

**ISP GROUP LLC на данный момент НЕ является licensed general contractor.**

Из этого следует:

1. Система ищет максимум возможностей, где ISP может участвовать законно: SUPPLIER, VENDOR, DISTRIBUTOR, SUBCONTRACTOR, SPECIALTY SERVICE PROVIDER, MATERIAL/EQUIPMENT/FURNITURE SUPPLIER.
2. Строительные тендеры **НЕ исключаются целиком**. Запрещено правило «construction = license = reject».
3. Требование лицензии определяется **только по документам конкретного opportunity** (solicitation, bid documents, instructions to bidders, SOW, применимые procurement-правила штата/города). Никогда не предполагается ни наличие лицензии у ISP, ни требование/отсутствие требования лицензии без проверки.
4. Заявки туда, где лицензия обязательна, НЕ подаются. Привлекательные лицензионные тендеры → статус **PARTNER REQUIRED**.

## Три стратегических направления

### Направление 1 — CONSTRUCTION SERVICES (без лицензии, где это законно)

Приоритетные категории: painting, drywall, flooring, tile, demolition, site cleanup, debris removal, pressure washing, landscaping, maintenance, minor repairs, installation (furniture/equipment/material), janitorial/facility services, moving, hauling, site services, specialty subcontracting, labor-intensive services, renovation-related services.

Каждый opportunity проходит **LICENSE CHECK**:

```
construction opportunity
        ↓
   analyze scope
        ↓
determine license requirement (по документам!)
        ↓
YES     → NO BID (учёт в отчёте LICENSE REQUIRED, топовые → PARTNER REQUIRED)
NO      → QUALIFIED
UNCLEAR → MANUAL REVIEW
```

### Направление 2 — SUPPLY

Отдельный engine для закупок товаров. Строительная лицензия для supply **не является автоматическим препятствием**.

Категории (расширяемые через config, без изменения кода):
- **Construction materials:** aggregate, granite, crushed stone, gravel, sand, concrete/road/fill/building/finishing materials
- **Construction equipment:** crane trucks, knuckle boom cranes, excavators, loaders, skid steers, forklifts, heavy equipment, material handling, specialized equipment
- **Furniture:** restaurant/commercial/hospitality/hotel furniture, tables, chairs, bar, outdoor, custom
- **General supplies**

### Направление 3 — SUBCONTRACTING / PRIME CONTRACTOR OUTREACH

Поиск prime contractors, general contractors, government contractors, facility management компаний, которые **получили или пытаются получить** контракты.

По каждому prime собирается: Company, Project, Agency, Solicitation, Award, Scope, Required materials/equipment/subcontractors, Procurement contact, Email, Phone, Website.

Затем определяется роль ISP: MATERIAL SUPPLY / EQUIPMENT SUPPLY / FURNITURE SUPPLY / NON-LICENSED SUBCONTRACTING / INSTALLATION / SPECIALTY SERVICES.

Источники: award-уведомления SAM.gov, USASpending API (primes по NAICS 236xxx/237xxx в целевых штатах), SBA SUBNet, DOT-lettings (кто выиграл дорожные контракты → кому нужен щебень), новости закупок.

## LICENSE INTELLIGENCE ENGINE (центральный модуль)

Модуль `license-check/` анализирует каждый opportunity направлений 1 и 3 (и supply-тендеры с элементами установки).

Схема записи:

| Поле | Значения |
|---|---|
| state / county / city / agency | география и заказчик |
| scope | краткое описание работ |
| trade | категория (painting, flooring…) |
| license_required | YES / NO / UNCLEAR |
| license_type | напр. FL Certified General Contractor, C-33 Painting (CA) |
| license_number_required | требуется ли номер в заявке |
| qualifier_required | нужен ли qualifier |
| bond_required / insurance_required | да/нет + суммы |
| notes | детали |
| source | ссылка на документ/правило — ОБЯЗАТЕЛЬНО |
| confidence | HIGH / MEDIUM / LOW |

Правила:
- Вердикт без указания `source` недопустим.
- `confidence: LOW` или противоречивые источники → всегда MANUAL REVIEW.
- База знаний по штатам/трейдам накапливается из проверенных вердиктов и переиспользуется, но каждый новый solicitation всё равно проверяется по своим документам (агентства вправе ставить требования выше законодательного минимума — напр., требовать лицензию там, где закон штата её не требует).

## Три независимых pipeline (CRM)

**PIPELINE A — CONSTRUCTION:** DISCOVERED → LICENSE CHECK → QUALIFIED → BID/NO BID → PRICING → SUBMISSION → AWAITING RESULT → WON / LOST. Дополнительные статусы: MANUAL REVIEW, NO BID, PARTNER REQUIRED.

**PIPELINE B — SUPPLY:** DISCOVERED → PRODUCT MATCH → SUPPLIER SEARCH → PRICING → QUOTE → SUBMISSION → AWAITING RESULT → WON / LOST.

**PIPELINE C — SUBCONTRACTING:** PRIME FOUND → CONTACT FOUND → OUTREACH → RESPONSE → RFQ RECEIVED → PRICING → QUOTE → NEGOTIATION → WON / LOST.

## Логика приоритетов

1. **Приоритет 1:** opportunities, выполнимые прямо сейчас без строительной лицензии (нелицензируемые services + всё направление supply с высоким fit).
2. **Приоритет 2:** supply opportunities.
3. **Приоритет 3:** subcontracting opportunities.
4. **Приоритет 4:** лицензионные construction opportunities с потенциалом партнёрства → **PARTNER REQUIRED** (не удалять!).

## LICENSED PARTNER STRATEGY

Для привлекательного opportunity с обязательной лицензией:
1. Статус PARTNER REQUIRED (не NO BID).
2. Поиск потенциального licensed contractor / qualifier / субподрядчика.
3. Карточка для решения: Project value, Scope, License required, Potential margin, Potential partner, Potential ISP role (supplier / equipment provider / material provider / subcontractor / project sourcing partner).

## FINAL SCORING v2 (0–100)

| Фактор | Вес |
|---|---|
| Product/service fit | 20 |
| **License feasibility** | **20** |
| Margin potential | 15 |
| Contract value | 10 |
| Competition | 10 |
| Delivery / execution feasibility | 10 |
| Buyer quality | 5 |
| Deadline | 5 |
| Strategic value | 5 |

Категории: **90–100 = A+**, **80–89 = A**, **70–79 = B**, **60–69 = C**, **<60 = NO PRIORITY**.

License feasibility: NO license required = 20; UNCLEAR = 8 (до manual review); YES + партнёрский потенциал = 4; YES без партнёра = 0.

## DAILY OUTPUT v2

Ежедневный отчёт содержит секции:
- TOP CONSTRUCTION OPPORTUNITIES (нелицензируемые/qualified)
- TOP SUPPLY OPPORTUNITIES
- TOP EQUIPMENT OPPORTUNITIES
- TOP FURNITURE OPPORTUNITIES
- TOP MATERIAL OPPORTUNITIES
- TOP SUBCONTRACTING OPPORTUNITIES
- PARTNER REQUIRED OPPORTUNITIES
- **LICENSE REQUIRED → NO BID** (отдельно: что мы теряем из-за отсутствия лицензии — метрика для решения о получении лицензии/партнёрствах)

## Следствия для площадок (поправка к аудиту PHASE 1)

Стратегия v2 повышает ценность каналов, которые в v1 были второстепенными:
- **SBA SUBNet** — прямой источник Pipeline C (subcontracting primes) → из «монитор» в активный ежедневный источник.
- **Bid Express / DOT lettings** — источники «кто выиграл дорожный контракт» → лид-ген primes для поставки щебня (Pipeline C), по-прежнему без платной подписки на старте.
- **USASpending API** — ядро Pipeline C: awards по NAICS 236xxx/237xxx в целевых штатах = список primes с контактами через SAM entity data.
- Городские/окружные порталы (DemandStar FL, PlanetBids CA, BidNet) — источник мелких нелицензируемых services (janitorial, debris removal, pressure washing, furniture installation) для Pipeline A.
- Реестры площадок и scoring платформ обновлены не пересчётом, а пометками ролей: платформа может кормить несколько pipelines одновременно.
