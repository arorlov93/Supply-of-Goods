# Шаблон запроса поставщику

Единственный разрешённый шаблон для писем поставщикам. Правила в
`CLAUDE.md`, раздел 1.

---

## Что в письме есть и чего в нём нет

**Есть:** позиции, количества, спецификация, почтовый индекс доставки,
срок поставки, срок ответа, условия оплаты, обещание повторных заказов.

**Нет и быть не может:** номера солиситации, слов «конкурс», «тендер»,
«заявка», «Лесная служба», «федеральный», имени конечного заказчика, даты
подачи заявки, UEI, CAGE, упоминания SAM и статуса малого бизнеса.

**Срок ответа обосновывается нашим планированием.** Не «у нас подача в
среду», а «во вторник закрывается наш закупочный цикл». Это правда: наш
цикл действительно закрывается тогда, когда нам нужно считать цену.

**Адрес доставки.** Даём улицу и индекс, без названия получателя. Без
адреса поставщик не посчитает фрахт, это допустимый минимум.

**Мотивация вместо вопроса.** Если поставщик сам торгует с государством,
мы его об этом не спрашиваем. Мы объясняем, почему продажа нам выгодна:
деньги без подготовки заявки, без удержания цены на 90 дней, без ведения
контракта и без ожидания государственной оплаты.

---

## Текст

```
Subject: RFQ [что] [количество] delivered [город, штат], quote needed by [день]

Good morning,

ISP GROUP LLC is a supply and trading company in Florida. We buy
[товарная группа] on a recurring basis and we are pricing a job now.

What we need:

1. [позиция, полная спецификация], [количество] each
2. [позиция], [количество] each
3. ...

Delivery: [улица], [город], [штат] [индекс]. Within [N] days of our
purchase order. There is offloading equipment on site and we will agree
the date and a window with you in advance.

Please quote:

1. Unit price for each line, FOB your plant or yard.
2. Freight to [индекс] as a separate lump sum, and how many trucks it
   takes. Or one delivered price per line, if that is simpler for you.
3. Lead time from purchase order to delivery.
4. Country of manufacture and the mill location of the material.
5. How long the price stays firm.
6. Your payment terms, and whether a deposit shortens the lead time.

Our purchasing cycle closes [день], so I need your numbers by then. If a
full quote on all lines is not possible in that time, price [самые
крупные позиции] alone and we will work from there. A telephone call is
just as good as an email, we are on (929) 830-0038.

If you work through distributors rather than selling direct, tell me who
covers [регион] and I will go to them.

This is not a one-off. We buy [товарная группа] regularly and we pay by
electronic transfer on our own terms, with no paperwork beyond a purchase
order and an invoice. If that is the kind of business you want more of,
say so and I will bring you the next ones first.

Thank you,

Aleksandr Orlov, Member
ISP GROUP LLC
16395 Biscayne Blvd Apt 818, Aventura, FL 33160-5743
(929) 830-0038
info@ispgroupgc.com
www.ispgroupgc.com
```

---

## Перевод на русский, чтобы было видно, что мы говорим

> Доброе утро.
>
> ISP GROUP LLC это снабженческая и торговая компания во Флориде. Мы
> регулярно закупаем [товарную группу] и сейчас считаем цену по объекту.
>
> Что нужно: [позиции с количествами].
>
> Доставка: [улица, город, штат, индекс], в течение [N] дней после нашего
> заказа. На площадке есть техника для разгрузки, дату и окно согласуем с
> вами заранее.
>
> Прошу дать: цену по каждой строке на условиях самовывоза; отдельно
> фрахт до индекса единой суммой и сколько машин, либо одну цену с
> доставкой, если так проще; срок изготовления; страну изготовления и
> завод, где выплавлен материал; как долго цена твёрдая; ваши условия
> оплаты и сокращает ли аванс срок.
>
> Наш закупочный цикл закрывается [день], значит цифры нужны к этому
> сроку. Если по всем строкам не успеваете, дайте цену по [крупным
> позициям], будем работать от них. Звонок подходит не хуже письма, мы на
> (929) 830-0038.
>
> Если вы работаете через дистрибьюторов, а не продаёте напрямую, скажите,
> кто закрывает [регион], и я пойду к ним.
>
> Это не разовая покупка. Мы берём [товарную группу] постоянно и платим
> банковским переводом по своим условиям, без бумаг сверх заказа и счёта.
> Если такой бизнес вам интересен, скажите, и следующие я принесу вам
> первым.

---

## Чем это отличается от того, что я отправил 10 и 12 октября

| Было | Стало |
|---|---|
| «We are preparing a quote for a Forest Service solicitation» | «we are pricing a job now» |
| «Our bid is due Wednesday 14 October at 10:00 Mountain Time» | «our purchasing cycle closes Tuesday» |
| «UEI WA46PAMTYMQ7, CAGE 217F4», «registered in SAM», «small business» | ничего из этого нет |
| «Forest Service Yard, 900 North 1100 East, Price UT» | «900 North 1100 East, Price, UT 84501» |
| **«Do you bid Forest Service solicitations directly yourselves?»** | **убрано полностью**, заменено на аргумент о выгоде работы с нами |
| ничего о повторных заказах | обещание следующих заказов, это делает нас интересным клиентом |
