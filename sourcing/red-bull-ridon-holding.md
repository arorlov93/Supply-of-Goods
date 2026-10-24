# Ridon Holding B.V.: проверка продавца

Проверено 24.10.2026. VIES, KvK, OpenStreetMap, собственные страницы
компании.

**Компания настоящая и проходит все проверки, которые провалил немецкий
продавец. Но она НЕ авторизованный дистрибьютор Red Bull, и это важно.**

---

# Реквизиты, подтверждённые

| Поле | Значение | Чем подтверждено |
|---|---|---|
| **Название** | **RIDON HOLDING B.V.** | **VIES, официально** |
| **НДС** | **NL802898531B01** | **VIES: `isValid: true`** |
| **KvK** | **27235695** | указан на их сайте, совпадает с OpenCorporates |
| **Адрес** | **Hoekeindseweg 146 A, 2665 KH Bleiswijk, Zuid-Holland, Нидерланды** | **VIES + карты** |
| Координаты | 51,9989 N, 4,5258 E | OpenStreetMap, тип `house` |
| Сайт | `rholdingbv.com` | работает |
| Торговля с | 2005 года, по данным каталогов | не подтверждено первоисточником |

## Главное отличие от немецкого случая

**Нидерланды в VIES раскрывают название и адрес, а Германия нет.** Ответ
VIES дословно:

```
"isValid" : true,
"name"    : "RIDON HOLDING B.V.",
"address" : "HOEKEINDSEWEG 00146 A
             2665KH BLEISWIJK"
```

**Это подтверждение от налоговой службы, а не с сайта продавца.** И их
собственный сайт совпадает с ним по номеру НДС и по адресу.

Сравнение двух продавцов по одним и тем же проверкам:

| Проверка | Германия, Woove GmbH | **Нидерланды, Ridon Holding** |
|---|---|---|
| сайт открывается | **нет**, пять способов | **да** |
| VIES, номер | валиден | валиден |
| **VIES, название и адрес** | **не раскрываются** | **ПОДТВЕРЖДЕНЫ** |
| реестровый номер на сайте | нет | **KvK 27235695** |
| следы в реестре | **не найдены** | KvK совпадает с OpenCorporates |
| адрес | **три варианта, один жилой** | **один, совпадает с VIES и картами** |
| партнёр по логистике | **не существует в заявленном виде** | организуют сами, базисы опубликованы |

## Одна мелочь по написанию адреса

На их собственном сайте стоит `HOEKEINSEWEG`, без буквы `d`. **В VIES и на
картах улица называется `Hoekeindseweg`.** В документах писать по VIES, это
первоисточник:

```
RIDON HOLDING B.V.
Hoekeindseweg 146 A
2665 KH Bleiswijk
Nederland
VAT NL802898531B01
KvK 27235695
```

Отдельно: в OpenCorporates как юридический адрес указан **Berkelse Poort
87, 2651 JX Berkel en Rodenrijs**. По картам это реальная коммерческая
зона. **Но VIES, то есть налоговая, даёт Блейсвейк, и сайт тоже. Рабочий
адрес Блейсвейк.** Расхождение уточнить в подтверждении заказа.

---

# Что они предлагают по Red Bull

С их страницы оптовой поставки, дословно:

> Bulk Red Bull Energy Drink for B2B buyers — available in **250ml, 355ml
> and 473ml cans**, including Sugarfree and Zero variants. **Sourced
> through established supplier channels** for wholesalers, distributors
> and retail chains, with **pallet-ready quantities** and worldwide
> delivery coordinated around your chosen Incoterms®.

| | |
|---|---|
| форматы | **250 мл**, 355 мл, 473 мл, плюс Sugarfree и Zero |
| объёмы | паллетами и контейнерами, `not individual units` |
| базисы | **EXW, FCA, FOB, CIF, DAP** |
| **цены** | **на сайте не публикуются, только по запросу** |
| оплата | **телеграфный перевод T/T на их счёт по проформе** |

---

# КРИТИЧЕСКОЕ: они не авторизованный дистрибьютор Red Bull

Ты написал, что они дистрибьюторы Red Bull. **Проверил: сами они этого
не утверждают.**

Их формулировки аккуратные и означают ровно обратное:

| Что написано у них | Что это значит |
|---|---|
| `our role as a **Red Bull wholesale supplier**` | оптовый поставщик, не дистрибьютор бренда |
| `**Sourced through established supplier channels**` | **закупают на открытом рынке у третьих лиц** |
| `**Verified Dutch trading company**` | торговая компания, а не назначенный дистрибьютор |

**Слова `authorized`, `official`, `appointed distributor` на их страницах
про Red Bull отсутствуют.** Единственное место, где стоит слово
`official`, это про их банковский счёт в разделе оплаты.

**Ярлык «дистрибьютор» взят из каталогов B2B** вроде TradeWheel и
FreshDI, где описание заполняет сама компания и где он ничего не
удостоверяет.

## Почему это принципиально для твоей задачи

Вся правовая конструкция держится на том, **где и с чьего согласия товар
впервые введён в оборот.**

Торговец, который «закупает через налаженные каналы поставщиков», **по
определению не может это удостоверить.** Он не знает и не обязан знать,
у кого купил его поставщик.

**Следствие: Ridon это ещё один европейский источник, и правовая стена
для России у него та же.** Товар, впервые проданный в ЕС, в ЕАЭС не
исчерпан, исключения по перечню параллельного импорта для кода 2202 нет.
Разбор в `red-bull-zakupka.md`.

И отдельный сигнал: **они торгуют форматами 473 мл и 335 мл, то есть
американскими и канадскими.** Это ровно та территория «материального
отличия товара», по которой Red Bull судится с серым импортом.

---

# Где они сильнее испанца

Одно реальное преимущество, и оно весомое.

**Блейсвейк это Южная Голландия, район Роттердама и Зутермеера, то есть
логистический центр Европы.** Карбальо это Галисия, атлантическое
побережье Испании.

| Откуда | Положение |
|---|---|
| **Bleiswijk, NL** | центр Европы, на основных коридорах |
| Carballo, ES | крайний северо-запад, самое дальнее плечо в Европе |

**Разница в плече до Восточной Европы примерно двукратная.** На банке это
несколько рублей, на фуре это десятки тысяч.

Плюс у них опубликованы базисы включая **DAP**, то есть можно получить
цену с доставкой и не брать на себя фуру.

---

# Что делать

## Запросить котировку, и теперь есть с чем сравнить

Цен они не публикуют, значит нужен запрос. **И у нас есть эталон,
установленный дважды независимо:**

| Ориентир | €/банка |
|---|---|
| **проверенный рынок на объёме фуры** | **0,88 - 0,90** |
| Испания, Sector Vending, 33 паллеты | 0,880 |
| Великобритания, трейдер, ящик | 0,8953 |

**Как читать их ответ:**

| Ответ Ridon | Вывод |
|---|---|
| **€0,85 - 0,95** | **нормально, это рынок** |
| €0,95 - 1,10 | дороже рынка, торговаться или брать испанца |
| **ниже €0,80** | **требовать объяснение.** Либо особая партия с коротким сроком, либо то же, что у немца |
| ниже €0,50 | **не платить.** Такой цены на этом рынке нет, расчёт в `red-bull-CENA-OKONCHATELNO.md` |

## Что обязательно спросить

1. цена за банку и за паллету на **33 паллеты, 85 536 банок**, формат
   **250 мл**, письменно, с датой действия;
2. **страна розлива и наличие кодировки партии** на банке;
3. **маркировка тары**: экспортная без логотипа системы залога, или
   немецкая DPG. Разница 23,72 ₽ на банку;
4. **остаточный срок годности** при отгрузке, в месяцах;
5. **подтверждение фактического наличия** 85 536 банок одной партией;
6. цена на базисе **EXW Bleiswijk** и отдельно **DAP** до точки;
7. **условия оплаты.** У них опубликован только телеграфный перевод по
   проформе, то есть предоплата. Спросить про аккредитив или оплату
   частями.

## И одно предостережение, несмотря на пройденные проверки

**Оплата у них только банковским переводом вперёд**, аккредитив на
страницах не упомянут. Компания проверена, но **первая сделка всё равно
не фурой.** Паллета или две, посмотреть товар, маркировку и документы, и
только потом объём. Проверка личности снижает риск, но не отменяет
правило первой маленькой сделки.

---

# ЗАПРОС КОТИРОВКИ: текст, НЕ ОТПРАВЛЕН

Правило 3: текст показан, отправка по отдельной команде.

**Кому:** через форму на `rholdingbv.com/contact-us/`. Отдельного адреса
отдела продаж на сайте нет, поэтому форма, и в тексте просьба ответить
письмом.

**Тема:**

```
Red Bull 250ml, full truck load: request for written quotation
```

**Текст:**

```
Dear Sir or Madam,

ISP GROUP LLC is a US registered trading company. We are sourcing Red
Bull Energy Drink 250ml in full truck load volume and would like a
written quotation.

VOLUME

  33 EUR pallets, which at 108 cases of 24 cans per pallet is
  85,536 cans. Please confirm whether your pallet configuration
  matches this, and correct the figures if it does not.

Please also quote 1 pallet and 2 pallets separately. Our first order
would be a trial pallet, not a full truck.

WHAT WE NEED IN THE QUOTATION

1. Price per can and per pallet, for the 250ml format, stated
   excluding VAT, and the date until which the price is valid.

2. Price on two bases side by side:
     EXW Bleiswijk
     DAP to a destination we will specify
   This lets us compare your delivered price against our own freight.

3. Confirmation that 85,536 cans of the 250ml format are actually
   available in one lot, and the lead time from order confirmation.

4. PRODUCT IDENTIFICATION. This is the most important point for us,
   because your TradeWheel listing shows 0.45 USD per can while
   European trade prices for the Austrian product are around 0.88 to
   0.90 EUR per can. Please state:
     - the EAN / barcode of the exact article you are quoting;
     - the country of filling and the filling plant;
     - whether the drink is carbonated or non-carbonated;
     - can or bottle, and the exact volume in ml;
     - the label language, and whether the can carries EU nutritional
       information;
     - whether batch coding is printed on the can.
   For reference, the Austrian Red Bull Energy Drink 250ml we are
   looking for carries EAN 9002490100070. If the article you offer has
   a different EAN, please say so plainly: we are interested in both,
   but they are different products for us and we must price them
   separately.

5. Can and tray marking. We specifically need to know whether the
   cans carry a deposit scheme logo, for example the German DPG
   logo, or whether they are export marked without it. This
   materially affects our landed cost.

6. Remaining shelf life at dispatch, in months.

7. Pallet data for freight planning: cases per pallet, cans per
   case, gross weight per pallet, pallet height, whether pallets are
   stackable, and whether EUR pallet exchange is required.

8. Payment terms. Your website states telegraphic transfer against
   proforma invoice. Please confirm whether you also work with a
   documentary letter of credit, or with part payment on order and
   the balance against shipping documents.

9. Documents you issue with the shipment: commercial invoice,
   packing list, CMR, certificate of origin.

ONE QUESTION ON DESTINATION, ASKED OPENLY

Before we specify the delivery destination, please tell us whether
you have any restrictions on destination countries for this product,
and whether any destinations require additional documentation on
your side. We would rather know your limits before we build a
calculation on them.

We would appreciate your reply by e-mail within five working days.

Kind regards,

ISP GROUP LLC
16395 Biscayne Blvd Apt 818, Aventura, FL 33160-5743
info@ispgroupgc.com, (929) 830-0038
```

## Почему письмо построено так

**Пункт 5 про маркировку тары стоит отдельным требованием**, потому что
немецкая тара с логотипом DPG добавляет €0,25, то есть **23,72 ₽ на
банку**, больше четверти цены товара. Это не деталь, это строка
себестоимости.

**Пункт 2 просит EXW и DAP рядом.** У них опубликован базис DAP, и если
их доставка окажется не дороже нашей фуры, то для первой сделки она
лучше: с нас снимается организация транспорта и риск в пути.

**Пункт 3 про фактическое наличие** нужен потому, что опубликованная
ступень по объёму и наличие этого объёма на складе это разные вещи. У
испанского продавца ступень на 3 564 ящика есть, а подтверждения наличия
нет.

**Пункт 8 про оплату.** На их сайте только телеграфный перевод по
проформе, то есть предоплата. Спрашиваем про аккредитив прямо, и ответ
сам по себе информативен: продавец, работающий с аккредитивом, сильно
отличается от продавца, работающего только по предоплате.

**Про первую паллету сказано в самом начале.** Это снимает неловкость
позже и сразу показывает, что мы не выдумываем объём, которого не
потянем.

## И про последний абзац, он сознательный

Я прошу их **назвать свои ограничения по странам назначения до того, как
мы назовём страну.**

Так правильнее по двум причинам. **Первая:** европейские продавцы с 2024
года проверяют конечного получателя, и часть из них отказывается от
отдельных направлений просто из осторожности. Узнать это одним вопросом
дешевле, чем после согласования цены и объёма. **Вторая:** если
ограничения есть, мы услышим их от продавца, а не будем строить расчёт на
предположении.

Правило 1 `CLAUDE.md` здесь не применяется: конкурса нет, забирать у нас
нечего, а скрытность в этом вопросе работает против нас, потому что
законность сделки зависит именно от происхождения товара и от того, что
продавец готов подтвердить документами.
