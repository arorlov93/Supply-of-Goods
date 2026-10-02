#!/usr/bin/env python3
"""Сколько нужно наценки, чтобы с оборота 7-10 млн/мес иметь 1-1,5 млн чистыми.

Налоговый контур 2026:
  НДС 22% (общая), либо спецставка 5% на УСН без вычетов (доход 20-272,5 млн/год)
  УСН «доходы минус расходы» 15%
  Порог освобождения от НДС на УСН — 20 млн/год, то есть при 84-120 млн/год НДС неизбежен
"""

USN = 0.15          # УСН доходы минус расходы
VAT_GEN = 0.22      # общая ставка
VAT_SPEC = 0.05     # спецставка без вычетов


def required_markup(revenue_gross, target_net, opex, mode, input_vat=True):
    """Какая закупочная цена (с НДС) допустима и какая нужна наценка."""
    pretax = target_net / (1 - USN)
    if mode == "gen":
        # доходы и расходы очищаются от НДС, входящий НДС к вычету
        rev_net = revenue_gross / (1 + VAT_GEN)
        cogs_net = rev_net - opex - pretax
        cogs_gross = cogs_net * (1 + VAT_GEN) if input_vat else cogs_net
    else:
        # спецставка: вычетов нет, входящий НДС сидит в себестоимости
        rev_net = revenue_gross / (1 + VAT_SPEC)
        cogs_gross = rev_net - opex - pretax
    if cogs_gross <= 0:
        return None
    return cogs_gross, revenue_gross / cogs_gross - 1, (revenue_gross - cogs_gross) / revenue_gross


def vat_crossover():
    """При какой валовой марже спецставка 5% выгоднее общей 22%."""
    a = VAT_SPEC / (1 + VAT_SPEC)          # НДС как доля выручки при спецставке
    b = VAT_GEN / (1 + VAT_GEN)            # НДС как доля добавленной стоимости
    return a / b


def net_from_markup(revenue_gross, markup, opex, mode):
    """Обратная задача: что останется при заданной наценке."""
    cogs_gross = revenue_gross / (1 + markup)
    if mode == "gen":
        base = revenue_gross / (1 + VAT_GEN) - cogs_gross / (1 + VAT_GEN) - opex
    else:
        base = revenue_gross / (1 + VAT_SPEC) - cogs_gross - opex
    return base * (1 - USN)


M = 1_000_000
print("=" * 72)
print("1. ТРЕБУЕМАЯ НАЦЕНКА ПОД ЦЕЛЬ (opex 500 тыс./мес)")
print("=" * 72)
print(f"{'оборот':>8}{'цель':>8}{'режим':>8}{'закупка':>12}{'наценка':>10}{'вал.маржа':>11}")
for rev in (7 * M, 8.5 * M, 10 * M):
    for tgt in (1.0 * M, 1.5 * M):
        for mode in ("gen", "spec"):
            r = required_markup(rev, tgt, 0.5 * M, mode)
            if r:
                cogs, mk, gm = r
                print(f"{rev/M:8.1f}{tgt/M:8.1f}{mode:>8}{cogs/M:12.3f}{mk*100:9.1f}%{gm*100:10.1f}%")

print()
print("=" * 72)
print("2. ГДЕ ПРОХОДИТ ГРАНИЦА МЕЖДУ СТАВКАМИ НДС")
print("=" * 72)
x = vat_crossover()
print(f"спецставка 5% выгоднее общей 22% при валовой марже выше {x*100:.1f}%")
print("ниже этого порога — общая 22% с вычетами (типичный случай для перепродажи)")

print()
print("=" * 72)
print("3. ЧТО РЕАЛЬНО ОСТАЁТСЯ ПРИ РЫНОЧНЫХ НАЦЕНКАХ (оборот 8,5 млн, opex 500 тыс.)")
print("=" * 72)
print(f"{'наценка':>9}{'вал.приб.':>12}{'чистыми 22%':>14}{'чистыми 5%':>13}  ниша")
niches = [(0.06, "канцелярия, бумага — аукцион"),
          (0.10, "канцелярия — ЗМО/котировки"),
          (0.15, "хозтовары, продукты — аукцион"),
          (0.22, "медрасходка, дезсредства"),
          (0.30, "соль/ПГМ при своей логистике"),
          (0.40, "узкий товар, мало поставщиков")]
for mk, name in niches:
    gross = 8.5 * M - 8.5 * M / (1 + mk)
    print(f"{mk*100:8.0f}%{gross/M:12.3f}{net_from_markup(8.5*M, mk, 0.5*M, 'gen')/M:14.3f}"
          f"{net_from_markup(8.5*M, mk, 0.5*M, 'spec')/M:13.3f}  {name}")

print()
print("=" * 72)
print("4. ОБОРОТНЫЙ КАПИТАЛ")
print("=" * 72)
print(f"{'цикл, дн':>10}{'оборот/мес':>13}{'заморожено':>13}")
for cycle in (30, 45, 60, 75):
    for rev in (8.5 * M,):
        print(f"{cycle:10}{rev/M:13.1f}{rev/30*cycle/M:13.1f}")
print("\nцикл = закупка и оплата поставщику -> поставка -> приемка (до 20 дн)")
print("      -> оплата заказчиком (7 рабочих дней по 44-ФЗ)")
