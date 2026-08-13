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
**Локации:** Florida (все) — снять California, если не нужен.
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
После сужения на FL и наши категории — это управляемый поток на ежедневный разбор из почты.

## Рабочая схема (принята)
BidNet шлёт совпадения на info@ispgroupgc.com → я читаю почту (доступ есть) → фильтрую по трейдам/FL →
qualified в план подачи. Скрейпинг SPA признан хрупким; email-канал надёжнее.

## Действие пользователя
Зайти в BidNet → Account → Notification Profile → выставить Florida + NIGP-категории выше.
После этого email-feed станет релевантным, и я буду вести из него ежедневный отбор.
