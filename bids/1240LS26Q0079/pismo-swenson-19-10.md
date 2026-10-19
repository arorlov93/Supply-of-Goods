# Письмо Swenson Supply от 19.10.2026: разбор

Пришло письмо от Gabe из Swenson Supply с приложенным письмом о
соответствии по трубам Манти-Ласаль, RFQ 1240LS26Q0079.

---

## 1. Закупка закрыта пять дней назад

Проверено по первоисточнику, не по памяти.

Исходная солиситация, строка 151:

> Offers are due at the email address above by 10:00 AM Mountain time on
> October 9, 2026.

Поправка 0002, строки 57-58:

> This amendment also **extends the response deadline to 10/14/2026 at
> 10:00 AM Mountain Time.** All other terms and conditions remain
> unchanged.

**Окно подачи закрылось в среду 14.10 в 10:00 по горному времени.**
Сегодня понедельник 19.10. Наша котировка на $86 335 так и осталась
неотправленным черновиком в почте.

Запись в SAM показывает `isActive: true` и дату архивации 29.10, но это
ни о чём не говорит: поле срока в записи пустое, а признак активности
держится до архивации независимо от того, закрылся приём предложений или
нет. Срок берётся из документа закупки, и он однозначен.

**Письмо опоздало на пять дней. Отправлять заявку сейчас нельзя: подача
после срока не рассматривается, а попытка её протолкнуть портит отношения
с контрактным специалистом, с которым нам ещё работать.**

## 2. Само письмо ничего не удостоверяет

Три дефекта, каждый сам по себе достаточен.

**Не подписано.** Пустая линия подписи, под ней «Authorized
Representative». Ни имени, ни должности, ни телефона, ни почты.

**Формулировки уклончивые.** Не «соответствует», а **«is represented as
meeting»**, то есть «заявляется как соответствующее». Не «изготовлено в
США», а **«are represented as manufactured in the United States»**. Это
пересказ чужого утверждения, а не утверждение.

**И прямо сказано, что это не удостоверение:**

> These statements are **subject to verification by the manufacturer's
> written certification** and country-of-origin documentation for the
> materials supplied.

То есть письмо отсылает за подтверждением к производителю. Для
требования Buy American в федеральной заявке нужна именно письменная
сертификация изготовителя, а Swenson это **склад, а не завод**: трубу,
которую они перепродают, делает ACE/Eaton Metals в Кирни, Небраска.

**Даже приди это письмо вовремя, оно бы требование по происхождению не
закрыло.**

## 3. По цене они нам не подходили и раньше

Из `sourcing/plan-zakupok.md`, замер 12.10:

| | |
|---|---|
| цена Swenson за 2 640 футов трубы | **$124 120** |
| что государство платило за то же в 2023 | $66 807 |
| разрыв | **+86 процентов** |
| их цена за фунт с доставкой | **$2,18** |
| наше правило отказа | **выше $1,45 за фунт не подаём** |

Вывод там записан дословно: **«124 120, розница, не берём»**. Они выше
нашего предела в полтора раза. Вся наша котировка на $86 335 была меньше,
чем Swenson просил за одну трубу.

## 4. Побочное наблюдение, важное для правил

В теме их письма стоит **`RE: Price, Utah Culvert Project — RFQ
1240LS26Q0079`**. Номер солиситации они знают, и знают они его потому,
что **мы сами его назвали** в переписке 10 и 12 октября, до того как
правило 1 в `CLAUDE.md` было введено.

Это и есть та утечка, от которой правило защищает: перепродавец без
федеральной истории теперь знает номер конкретной закупки Лесной службы и
то, что мы по ней считали цену. Здесь обошлось, потому что закупка
закрылась. **На действующей закупке такое стоило бы контракта.**

Шаблон `sourcing/rfq/SHABLON-zapros-postavshchiku.md` это уже
фиксирует, в нём есть разбор отличий от писем 10 и 12 октября.

## 5. Что из этого всё-таки ценно

Swenson **ответил сам, без напоминания, через неделю.** ACE/Eaton, Lane
Enterprises, St. Regis Culvert, TrueNorth и Metal Culverts, которым мы
писали 12.10, молчат до сих пор. Отзывчивый поставщик это актив, даже
если его прайс розничный.

А розничный прайс это решаемая проблема, и план это уже говорит:

> Разрыв объясняется не дорогим производством, а тем, что нам дают
> розницу. У победителей этих закупок есть торговые счета со скидкой 30
> до 45 процентов от прайса, у нас нет.
> **Вывод: главное вложение не в поиск, а в открытие счетов.**

Скидка 30-45 процентов от $2,18 это **$1,20 - 1,53 за фунт**, то есть
ровно наш коридор. **Один дилерский счёт у Swenson переводит их из
«не берём» в «рабочий поставщик».**

В плане на месяц ещё четыре закупки, где нужна труба и прокат. Счёт
нужен к ним, а не к этой.

---

## Ответ Gabe: текст на согласование, НЕ отправлен

По правилу 3 показываю в диалоге, отправка по отдельной команде.

Что в письме есть: благодарность, честное закрытие темы по Юте, просьба
о кредитной заявке и о цене за фунт на условиях завода.

Что в письме нет: номеров других закупок, названий заказчиков, сроков
подачи, упоминания конкурсов. Про Юту номер назван только потому, что он
уже в их собственной теме и закупка закрыта.

```
Hi Gabe,

Thank you for following up, and for the letter.

Straight answer on the Utah job: the response deadline was 10:00 AM
Mountain on 14 October, so that one is closed. Nothing further is needed
for it.

Two things would be worth more to me than that job was.

First, your credit application. We are a supply and trading company and
we buy corrugated pipe, coupling bands and steel on a recurring basis. We
pay by electronic transfer and we would rather be set up on an account
before the next requirement lands than scramble when it does. Send me the
form and the documents you need from us and I will turn it around the
same day.

Second, pricing on a dealer basis. On the Utah quantity your number came
to about $2.18 per pound delivered. That is a retail number and it does
not clear our ceiling. What I need to see going forward is your dealer
column: price per pound FOB mill, freight quoted separately, and the lead
time from purchase order. If the mill is ACE in Kearney, tell me so
plainly and I will take the freight into my own calculation rather than
guessing at it.

One note on the compliance letter, said plainly so there is no confusion
later. As written it states that the pipe "is represented as" meeting
AASHTO M 36 and "is represented as" manufactured in the USA, and it makes
those statements subject to verification by the manufacturer. For the
work we do, origin has to be certified by the mill in writing, on the
mill's letterhead, naming the heat or lot. If you can get that from your
mill as a matter of routine, say so, because that alone decides whether
we can use a supplier.

We have four more requirements for pipe and steel in the next several
weeks. I would rather bring them to someone who answers his email, and
you did.

Thank you,

Aleksandr Orlov, Member
ISP GROUP LLC
16395 Biscayne Blvd Apt 818, Aventura, FL 33160-5743
(929) 830-0038
info@ispgroupgc.com
www.ispgroupgc.com
```
