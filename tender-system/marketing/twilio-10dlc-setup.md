# TWILIO 10DLC — настройка warm-SMS follow-up для ISP GROUP
Цель: слать SMS ТОЛЬКО тёплым (кто ответил/дал номер/согласился). Cold SMS — запрещены (TCPA).

## Почему 10DLC
Для бизнес-SMS с обычного 10-значного номера в США оператор требует регистрацию **10DLC**
(A2P): Brand (компания) + Campaign (тип сообщений). Без неё несущие блокируют/фильтруют SMS.
Регистрация ~1–3 дня, разовая + мелкая абонплата.

## ШАГИ (делает пользователь; я подключу отправку после)
1. **Аккаунт Twilio:** twilio.com → Sign up (info@ispgroupgc.com). Пополнить баланс ($20 хватит на старт).
2. **Купить номер:** Phone Numbers → Buy a number → локальный (305 Майами / 415 SF / 213 LA),
   с поддержкой SMS. ~$1–2/мес.
3. **A2P 10DLC регистрация** (Messaging → Regulatory Compliance → A2P 10DLC):
   - **Brand:** ISP GROUP LLC · EIN 38-4380828 · адрес Aventura FL · сайт ispgroupgc.com ·
     тип: Standard/Low-Volume (для нашего объёма достаточно Low-Volume — дешевле, до ~6k сообщений/день).
   - **Campaign:** use-case **«Customer Care / Mixed»** (follow-up по запросам подрядчиков).
     Sample messages (примеры для модерации):
       • "Hi [Name], ISP Group here — following up on the quote you requested for [project]. Reply STOP to opt out."
       • "Hi [Name], confirming we can price your [scope] this week. Want me to send the estimate? Reply STOP to opt out."
     Opt-in описание: «Recipients are business contacts who replied to our email or provided their
     number requesting a quote/callback.» Opt-out: STOP. Help: HELP.
4. **API-ключ:** Account → API keys → создать; прислать мне **Account SID + Auth Token (или API Key/Secret)
   + номер отправителя**. Сохраню в .env (не в git), как ключ Brevo.

## КАК АГЕНТ БУДЕТ СЛАТЬ (compliance встроен)
- SMS уходит ТОЛЬКО контактам со статусом WARM (ответил на письмо / оставил номер / отметил «call/text me»).
- Каждое SMS: имя ISP + суть + «Reply STOP to opt out». STOP → статус SMS_OPTOUT (навсегда).
- Частота: не чаще 1 SMS + 1 напоминание; бизнес-часы получателя.
- Никаких холодных номеров из пермитов в SMS — только звонок человеком, а SMS уже после контакта.
- Логи всех SMS — как sent-log для email.

## СТОИМОСТЬ (ориентир)
Номер ~$1–2/мес · SMS ~$0.0079/шт · 10DLC Low-Volume Brand ~$4 разово + campaign ~$1.5–10/мес.
Для follow-up тёплых (десятки-сотни SMS/мес) — копейки.

## ГРАНИЦА (жёстко)
10DLC/Twilio НЕ превращает cold SMS в легальные. Массовая холодная SMS-рассылка = нарушение TCPA
и правил оператора (бан кампании). SMS = только warm follow-up. Точка.
