# Kasbiy Ta'lim Ishonch Boti

Rasmiy murojaatlar boti — Qoraqalpog'iston Respublikasi Kasbiy ta'limni
rivojlantirish boshqarmasi uchun.

Telegram: **@kasbiytalim_ishonch_qqr_bot**

## Imkoniyatlar

- 3 tilda ishlash: 🇺🇿 O'zbekcha, 🇰🇷 Qoraqalpoqcha, 🇷🇺 Ruscha
- 🚨 Korrupsiya haqida anonim yoki shaxsiy murojaat (matn + foto/video/hujjat/ovoz)
- 💬 Taklif va murojaatlar
- ☎️ Aloqa ma'lumotlari va joylashuv
- ℹ️ Bot haqida ma'lumot
- Har bir murojaat administratorga (`ADMIN_ID`) avtomatik yuboriladi, o'z ID
  raqami bilan (masalan `CR-000001`)
- `/admin` — statistikalar, SQLite/CSV eksport, ID bo'yicha qidirish,
  foydalanuvchiga javob yozish, murojaat holatini o'zgartirish
- Spam-dan himoya (rate limiting), fayl hajmi tekshiruvi, HTML escaping
- Har kunlik loglar (`logs/bot.log`, `logs/errors.log`)

## Loyiha tuzilishi

```
project/
│
├── bot.py                # Kirish nuqtasi (long polling)
├── config.py              # .env dan konfiguratsiya
├── database.py             # aiosqlite ustida async DB qatlami
├── requirements.txt
├── render.yaml
├── Procfile
├── Dockerfile
├── .env.example
├── README.md
│
├── handlers/               # aiogram routerlar
├── keyboards/              # reply/inline klaviaturalar
├── states/                 # FSM holatlari
├── services/                # notify.py, export.py
├── utils/                  # texts.py (i18n), logger, validators, middleware
├── database/                # schema.sql (SQL sxema fayli)
├── media/exports/            # eksport qilingan CSV/DB fayllar
└── logs/                    # runtime loglar
```

## 1. Bot yaratish (BotFather)

1. Telegramda [@BotFather](https://t.me/BotFather) ga o'ting.
2. `/newbot` buyrug'ini yuboring va ko'rsatmalarga amal qiling.
3. Username sifatida `kasbiytalim_ishonch_qqr_bot` bering (agar band bo'lmasa).
4. BotFather bergan **tokenni** saqlab qo'ying.

## 2. Muhit sozlamalari

```bash
cp .env.example .env
```

`.env` faylini oching va to'ldiring:

```
BOT_TOKEN=123456:ABC-your-real-token
ADMIN_ID=5392733969
DATABASE=database.db
```

`ADMIN_ID` — statistikani ko'rish, eksport qilish va murojaatlarga javob
berish huquqiga ega bo'lgan administratorning Telegram user ID raqami
(o'zining ID sini bilish uchun [@userinfobot](https://t.me/userinfobot) dan
foydalanishingiz mumkin).

## 3. Lokal ishga tushirish

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

Birinchi ishga tushirishda `database.db` va `database/schema.sql` asosida
kerakli jadvallar avtomatik yaratiladi.

## 4. Docker orqali ishga tushirish (ixtiyoriy)

```bash
docker build -t kasbiy-talim-bot .
docker run --env-file .env -v $(pwd)/database.db:/app/database.db kasbiy-talim-bot
```

## 5. Render.com ga deploy qilish

1. Loyihani GitHub repositoriyasiga yuklang.
2. Render.com da **New + → Blueprint** ni tanlang va repo manzilini bering —
   `render.yaml` avtomatik o'qiladi (worker turi, disk va env o'zgaruvchilar
   bilan birga).
3. Render dashboard’da quyidagi maxfiy o'zgaruvchilarni to'ldiring:
   - `BOT_TOKEN`
   - `CONTACT_PHONE`, `CONTACT_EMAIL`, `CONTACT_WEBSITE`, `CONTACT_ADDRESS`,
     `CONTACT_LATITUDE`, `CONTACT_LONGITUDE`
4. `render.yaml` `/var/data` yo'lida 1 GB persistent disk biriktiradi, shunda
   `database.db` har bir deploy'dan keyin ham saqlanib qoladi.
5. Deploy tugagach, worker avtomatik ravishda long-polling rejimida ishga
   tushadi (webhook yoki port kerak emas).

> **Eslatma:** Bu loyiha long-polling orqali ishlaydi, shuning uchun Render’da
> **Background Worker** turi tanlangan — HTTP portini ochish shart emas.

## Admin panel (`/admin`)

Faqat `ADMIN_ID` bilan mos keluvchi foydalanuvchi uchun ochiladi:

- 📊 Statistika — foydalanuvchilar, bugungi/jami murojaatlar, anonim/shaxsiy/
  taklif sonlari
- 📁 Export DB — `database.db` faylini to'g'ridan-to'g'ri yuboradi
- 📄 Export CSV — barcha murojaatlarni CSV formatida eksport qiladi
- 🔍 ID bo'yicha qidirish — masalan `CR-000001`
- ✉️ Foydalanuvchiga javob — murojaat ID si orqali foydalanuvchiga xabar
  yuborish
- 🔄 Status o'zgartirish — Yangi / Jarayonda / Hal qilindi / Rad etildi

## Xavfsizlik

- Token va admin ID hech qachon kodga yozilmagan — faqat `.env` orqali
- Xabarlar orasidagi minimal interval (`RATE_LIMIT_SECONDS`) spamni cheklaydi
- Yuklanadigan fayllar hajmi `MAX_UPLOAD_MB` bilan chegaralangan
- Foydalanuvchi matni administratorga yuborishdan oldin HTML-escape qilinadi
- Foydalanuvchi ma'lumotlari faqat administratorga yuboriladi, ochiq
  ko'rinishda hech qayerda saqlanmaydi/chop etilmaydi

## Litsenziya

Ushbu loyiha Qoraqalpog'iston Respublikasi Kasbiy ta'limni rivojlantirish
boshqarmasi uchun ishlab chiqilgan.
