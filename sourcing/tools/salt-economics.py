#!/usr/bin/env python3
"""Юнит-экономика соли из Казахстана при закупке 4 500 ₽/т.

Цена контракта — с НДС (44-ФЗ: цена контракта включает все налоги).
Ввозной НДС из ЕАЭС платится в ФНС до 20-го числа месяца, следующего за принятием
на учёт, и принимается к вычету ТОЛЬКО на общей ставке 22%.
"""
BUY = 4500          # ₽/т, ввоз со всеми документами (со слов заказчика)
VAT = 0.22
USN = 0.15


def per_ton(contract_price, buy=BUY, delivery=0, buy_includes_vat=False, mode="gen"):
    """Валовая прибыль с тонны, ₽ (без учёта постоянных расходов)."""
    if mode == "gen":
        rev = contract_price / (1 + VAT)                 # выручка без НДС
        if buy_includes_vat:
            cost = buy / (1 + VAT)                       # ввозной НДС к вычету
        else:
            cost = buy                                   # ввозной НДС сверху, но возвращается
        cost += delivery / (1 + VAT)                     # перевозка от НДС-ника
    else:                                                # спецставка 5% без вычетов
        rev = contract_price / 1.05
        cost = (buy if buy_includes_vat else buy * (1 + VAT)) + delivery
    return rev - cost


def show(contract_price, label):
    print(f"\n{label}: цена контракта {contract_price:,} ₽/т (с НДС)")
    print(f"{'доставка':>10}{'вал.приб. 22%':>15}{'маржа':>8}{'вал.приб. 5%':>14}{'маржа':>8}")
    for dl in (0, 500, 1000, 1500, 2000):
        g = per_ton(contract_price, delivery=dl, mode="gen")
        s = per_ton(contract_price, delivery=dl, mode="spec")
        print(f"{dl:>10}{g:>15,.0f}{g/(contract_price/1.22)*100:>7.0f}%"
              f"{s:>14,.0f}{s/(contract_price/1.05)*100:>7.0f}%")


print("=" * 64)
print(f"ЗАКУПКА {BUY:,} ₽/т, ввозной НДС сверх цены и принимается к вычету")
print("=" * 64)
show(7950, "Якорь: Рязань 2 000 т / 15,9 млн")
show(7000, "Если сторговались до")
show(6000, "Жёсткий аукцион")

print("\n" + "=" * 64)
print("МЕСЯЧНЫЙ ПЛАН под оборот 8,5 млн ₽ при цене 7 950 ₽/т")
print("=" * 64)
tons = 8_500_000 / 7950
print(f"нужно поставить: {tons:,.0f} т/мес = {tons/66:.1f} вагонов по 66 т")
for dl in (500, 1000, 1500):
    gp = per_ton(7950, delivery=dl) * tons
    for opex in (400_000, 600_000):
        net = (gp - opex) * (1 - USN)
        print(f"  доставка {dl:>4} ₽/т · opex {opex//1000:>3} тыс. → "
              f"вал.приб. {gp/1e6:5.2f} млн, чистыми {net/1e6:5.2f} млн")

print("\n" + "=" * 64)
print("ОБОРОТКА И ВВОЗНОЙ НДС")
print("=" * 64)
month_buy = tons * BUY
imp_vat = month_buy * VAT
print(f"закупка товара на месяц: {month_buy/1e6:.2f} млн ₽")
print(f"ввозной НДС 22% в ФНС:   {imp_vat/1e6:.2f} млн ₽ — платится до 20-го числа")
print(f"                          следующего месяца, ДО оплаты заказчиком")
print(f"итого пиковая потребность: {(month_buy + imp_vat)/1e6:.2f} млн ₽ на цикл")
print(f"при цикле 45 дней:         {(month_buy + imp_vat)*1.5/1e6:.2f} млн ₽")
