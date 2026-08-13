# BidNet Direct — доступ и настройка профиля (13.08.2026)

## Доступ
- Вход: https://www.bidnetdirect.com/login (прямой, SAML SSO, БЕЗ капчи — автоматизируется)
- Логин: info@ispgroupgc.com · пароль в `.env` (BIDNET_USER/BIDNET_PASS, не в git)
- План: **Free tier** — часть тендеров помечена «upgrade required» (полный доступ платный). Флоридская группа (Florida Purchasing Group) видна.
- Сессию можно поднимать заново каждый цикл из .env; браузер — Chromium через прокси (нужна enterprise-policy PostQuantum off: /etc/chromium/policies/managed/isp.json).

## ⚠️ ПРОБЛЕМА: профиль уведомлений настроен не под ISP
Текущий feed (примеры за 3 дня): Novato Blvd (CA), Visalia gym flooring (CA), Tiburon play area (CA),
Callaway paving (FL, дорога — не наш трейд), Miami Beach entrance signs (FL, не наш трейд),
Seminole mold remediation (FL, лицензируемо). → нерелевантно.

Причина: NIGP-категории/локации в notification profile не соответствуют нашим услугам.

## Что настроить в профиле (рекомендация)
**Локации (директива пользователя 13.08): CA + FL, оба штата, основные города — к локации НЕ привязаны.**
Оставить обе Purchasing Groups (California + Florida), приоритет крупных метро:
FL — Miami-Dade, Broward, Palm Beach, Orlando, Tampa, Jacksonville; CA — LA, San Diego, Bay Area, Sacramento.
Фильтруем НЕ по штату, а ПО ТРЕЙДУ (NIGP ниже).
**NIGP-категории под наши трейды:**
- 910/912 — Building Maintenance, Janitorial/Custodial
- 988 — Landscaping / Grounds Maintenance
- 909 — Painting/Waterproofing
- 631 — Flooring materials/installation
- 425 — Furniture
- 750 — Aggregates/Road materials (для Pipeline C supply)
- Debris removal / hauling; pressure washing

**Объёмы на BidNet по ключевым словам (весь доступный охват, CA+FL):**
cleaning 225 · landscaping 149 · painting 136 · flooring 117 · debris 104 · aggregate 35 ·
janitorial 33 · furniture 28 · stucco 18 · grounds maintenance 13 · pressure washing 7.
Это управляемый поток на ежедневный разбор из почты (оба штата).

## Важно: услуги vs поставка при работе в двух штатах
- **Поставка** (мебель 425, материалы/aggregate 750, оборудование) — география НЕ ограничивает: отгружаем в любой штат. CA-тендеры на furniture/supply берём наравне с FL.
- **Услуги** (cleaning, painting, flooring install, landscaping) — нужна бригада на месте. В FL (Miami-Dade база) — свои силы; в CA — только через локального суб-исполнителя или как поставка материалов. В отбор берём, но помечаем «CA services → нужен местный суб».

## Рабочая схема (принята)
BidNet шлёт совпадения на info@ispgroupgc.com → я читаю почту (доступ есть) → фильтрую ПО ТРЕЙДУ (оба штата) →
qualified в план подачи (supply — везде; services CA — с пометкой про местную бригаду). Email-канал надёжнее скрейпинга SPA.

## Действие пользователя
BidNet → Account → Notification Profile → оставить California + Florida, добавить NIGP-категории выше
(сейчас профиль ловит случайное — дорожные CA + нерелевантное FL). После этого email-feed станет релевантным.
