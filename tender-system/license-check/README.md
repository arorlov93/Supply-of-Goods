# LICENSE INTELLIGENCE ENGINE (LICENSE_CHECKER)

Центральный модуль системы. Анализирует лицензионные требования каждого construction/services opportunity (и supply-тендеров с элементами установки) **по документам конкретной закупки**.

## Запрещено

- Предполагать наличие лицензий у ISP GROUP LLC (их нет: `COMPANY_LICENSES: []`).
- Утверждать «требуется / не требуется лицензия» без проверки solicitation, bid documents, instructions to bidders, SOW и применимых правил штата/округа/города.
- Автоматический reject строительных тендеров без license check.
- Подавать заявки, где лицензия обязательна.

## Алгоритм

1. Извлечь scope работ из документов opportunity.
2. Найти в документах явные требования: "contractor license", "license number", "certified", "registered contractor", qualifier, bond, insurance.
3. Если документы молчат — проверить применимое право: лицензионные требования штата (напр. FL DBPR/CILB, CA CSLB, NY/NJ local licensing) и муниципальные правила для данного trade. Каждый факт — со ссылкой.
4. Вынести вердикт с confidence и source.

## Вердикты и действия

| license_required | confidence | Действие |
|---|---|---|
| YES | HIGH/MEDIUM | NO BID; если score ≥ 70 → PARTNER REQUIRED |
| NO | HIGH | QUALIFIED → в pipeline дальше |
| NO | MEDIUM/LOW | MANUAL REVIEW |
| UNCLEAR | любая | MANUAL REVIEW |

## Схема записи (verdicts/*.yaml)

```yaml
opportunity_id: ""
state: ""
county: ""
city: ""
agency: ""
scope: ""
trade: ""            # painting | flooring | demolition | ...
license_required: "" # YES | NO | UNCLEAR
license_type: ""     # напр. FL Certified General Contractor; CA C-33 Painting
license_number_required: null   # true/false
qualifier_required: null
bond_required: null   # false или сумма/условие
insurance_required: null
notes: ""
source: ""           # ОБЯЗАТЕЛЬНО: ссылка на документ solicitation или норму права
confidence: ""       # HIGH | MEDIUM | LOW
checked_at: ""
result: ""           # NO_BID | QUALIFIED | MANUAL_REVIEW | PARTNER_REQUIRED
```

Примеры формата (иллюстрация, НЕ проверенные факты):
- Painting / Florida / License required: NO / Confidence: HIGH → QUALIFIED
- General building contractor / Florida / License required: YES / Confidence: HIGH → NO BID
- Floor installation / Florida / License required: UNCLEAR → MANUAL REVIEW

## База знаний (`knowledge-base/`)

Проверенные вердикты по парам «штат/муниципалитет × trade» накапливаются и переиспользуются как подсказка первого приближения. Но каждый новый solicitation всё равно проверяется по своим документам: агентство вправе требовать больше, чем законодательный минимум (например, требовать лицензию или бонд там, где закон штата их не требует). База стартует пустой — наполняется только verified-записями с источниками.

## PARTNER REQUIRED (Licensed Partner Strategy)

Для лицензионного opportunity с высоким score создаётся карточка `partner-required/<id>.md`:
- Project value / Scope / License required (тип)
- Potential margin
- Potential partner (найденные licensed contractors / qualifiers)
- Potential ISP role: supplier | equipment provider | material provider | subcontractor | project sourcing partner

Решение о партнёрстве и любые соглашения — только пользователь.
