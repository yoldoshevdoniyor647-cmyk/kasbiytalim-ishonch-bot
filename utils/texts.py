"""Centralized i18n strings for Uzbek (uz), Qoraqalpoq (kaa) and Russian (ru).

Usage:
    from utils.texts import t
    text = t("welcome", lang)
"""
from __future__ import annotations

SUPPORTED_LANGUAGES = ("uz", "kaa", "ru")

LANGUAGE_NAMES = {
    "uz": "🇺🇿 O'zbekcha",
    "kaa": "🇰🇷 Qaraqalpaqsha",
    "ru": "🇷🇺 Русский",
}

LANGUAGE_CODE_BY_NAME = {name: code for code, name in LANGUAGE_NAMES.items()}

TEXTS: dict[str, dict[str, str]] = {
    "choose_language": {
        "uz": "Tilni tanlang / Assalomu alaykum!",
        "kaa": "Tildi tańlań!",
        "ru": "Выберите язык:",
    },
    "welcome": {
        "uz": (
            "Assalomu alaykum!\n\n"
            "Qoraqalpog'iston Respublikasi Kasbiy ta'limni rivojlantirish "
            "boshqarmasining rasmiy murojaatlar botiga xush kelibsiz."
        ),
        "kaa": (
            "Assalawma áleykum!\n\n"
            "Qaraqalpaqstan Respublikasi Kásiplik bilimlendiriwdi rawajlandırıw "
            "basqarmasınıń rásmiy murájat botına qош keldińiz."
        ),
        "ru": (
            "Здравствуйте!\n\n"
            "Добро пожаловать в официальный бот обращений Управления развития "
            "профессионального образования Республики Каракалпакстан."
        ),
    },
    "language_changed": {
        "uz": "Til muvaffaqiyatli o'zgartirildi.",
        "kaa": "Til sátti ózgertildi.",
        "ru": "Язык успешно изменён.",
    },
    "menu_corruption": {
        "uz": "🚨 Korrupsiya haqida xabar berish",
        "kaa": "🚨 Korrupciya haqqında xabar beriw",
        "ru": "🚨 Сообщить о коррупции",
    },
    "menu_suggestion": {
        "uz": "💬 Taklif va murojaat",
        "kaa": "💬 Usınıs hám murájat",
        "ru": "💬 Предложение и обращение",
    },
    "menu_contact": {
        "uz": "☎️ Aloqa",
        "kaa": "☎️ Baylanıs",
        "ru": "☎️ Контакты",
    },
    "menu_about": {
        "uz": "ℹ️ Bot haqida",
        "kaa": "ℹ️ Bot haqqında",
        "ru": "ℹ️ О боте",
    },
    "menu_language": {
        "uz": "🌐 Tilni o'zgartirish",
        "kaa": "🌐 Tildi ózgertiw",
        "ru": "🌐 Изменить язык",
    },
    "choose_report_type": {
        "uz": "Murojaat turini tanlang:",
        "kaa": "Murájat túrin tańlań:",
        "ru": "Выберите тип обращения:",
    },
    "btn_anonymous": {
        "uz": "✅ Anonim murojaat",
        "kaa": "✅ Anonim murájat",
        "ru": "✅ Анонимное обращение",
    },
    "btn_personal": {
        "uz": "👤 O'zim haqimda ma'lumot beraman",
        "kaa": "👤 Óz mағlıwmatımdı beremen",
        "ru": "👤 Укажу свои данные",
    },
    "ask_report_text": {
        "uz": "Iltimos, murojaatingizni yozing.",
        "kaa": "Iltimas, murájatıńızdı jazıń.",
        "ru": "Пожалуйста, опишите вашу проблему текстом.",
    },
    "ask_evidence": {
        "uz": "Isbot (dalil) biriktirmoqchimisiz?",
        "kaa": "Dálil biriktiriwdi qálaysız ba?",
        "ru": "Хотите приложить доказательства?",
    },
    "btn_photo": {"uz": "📷 Foto", "kaa": "📷 Photo", "ru": "📷 Фото"},
    "btn_video": {"uz": "🎥 Video", "kaa": "🎥 Video", "ru": "🎥 Видео"},
    "btn_document": {"uz": "📄 Hujjat", "kaa": "📄 Hújjet", "ru": "📄 Документ"},
    "btn_voice": {"uz": "🎤 Ovozli xabar", "kaa": "🎤 Dawıslıq xabar", "ru": "🎤 Голосовое"},
    "btn_skip": {"uz": "⏭ O'tkazib yuborish", "kaa": "⏭ Ótkerip jiberiw", "ru": "⏭ Пропустить"},
    "evidence_received": {
        "uz": "Qabul qilindi. Yana fayl yuborishingiz yoki davom etishingiz mumkin.",
        "kaa": "Qabıl etildi. Tағы fayl jiberiwińiz yamasa dawam etiwińiz múmkin.",
        "ru": "Принято. Можете отправить ещё файл или продолжить.",
    },
    "ask_send_confirm": {
        "uz": "Murojaatni yuborishni tasdiqlaysizmi?",
        "kaa": "Murájattı jiberiwdi tastıyıqlaysız ba?",
        "ru": "Подтвердите отправку обращения.",
    },
    "btn_send": {"uz": "✅ Yuborish", "kaa": "✅ Jiberiw", "ru": "✅ Отправить"},
    "btn_cancel": {"uz": "❌ Bekor qilish", "kaa": "❌ Biykar etiw", "ru": "❌ Отмена"},
    "report_sent": {
        "uz": "Rahmat! Murojaatingiz qabul qilindi. Murojaat raqami: {code}",
        "kaa": "Raxmet! Murájatıńız qabıl etildi. Murájat nomeri: {code}",
        "ru": "Спасибо! Ваше обращение принято. Номер обращения: {code}",
    },
    "report_cancelled": {
        "uz": "Murojaat bekor qilindi.",
        "kaa": "Murájat biykar etildi.",
        "ru": "Обращение отменено.",
    },
    "ask_full_name": {
        "uz": "Ism-familiyangizni kiriting:",
        "kaa": " Atı-familiyańızdı kiritiń:",
        "ru": "Введите ваше полное имя:",
    },
    "ask_phone": {
        "uz": "Telefon raqamingizni kiriting (masalan: +998901234567):",
        "kaa": "Telefon nomerińizdi kiritiń (mısalı: +998901234567):",
        "ru": "Введите ваш номер телефона (например: +998901234567):",
    },
    "invalid_phone": {
        "uz": "Telefon raqami noto'g'ri. Qaytadan kiriting (masalan: +998901234567):",
        "kaa": "Telefon nomeri qáte. Qayta kiritiń (mısalı: +998901234567):",
        "ru": "Неверный формат номера. Введите ещё раз (например: +998901234567):",
    },
    "ask_organization": {
        "uz": "Tashkilot nomini kiriting:",
        "kaa": "Mákeme atın kiritiń:",
        "ru": "Введите название организации:",
    },
    "ask_district": {
        "uz": "Tumaningizni kiriting:",
        "kaa": "Rayonıńızdı kiritiń:",
        "ru": "Введите ваш район:",
    },
    "ask_suggestion_text": {
        "uz": "Taklif yoki murojaatingizni yozing:",
        "kaa": "Usınıs yamasa murájatıńızdı jazıń:",
        "ru": "Напишите ваше предложение или обращение:",
    },
    "suggestion_sent": {
        "uz": "Rahmat! Taklifingiz qabul qilindi. Murojaat raqami: {code}",
        "kaa": "Raxmet! Usınısıńız qabıl etildi. Murájat nomeri: {code}",
        "ru": "Спасибо! Ваше предложение принято. Номер обращения: {code}",
    },
    "about_text": {
        "uz": (
            "🏛 <b>Kasbiy Ta'lim Ishonch Boti</b>\n\n"
            "Ushbu bot Qoraqalpog'iston Respublikasi Kasbiy ta'limni "
            "rivojlantirish boshqarmasi tomonidan fuqarolardan korrupsiya "
            "holatlari, takliflar va murojaatlarni qabul qilish maqsadida "
            "yaratilgan.\n\n"
            "🔒 Anonim murojaatlar to'liq maxfiy saqlanadi. Sizning "
            "shaxsiy ma'lumotlaringiz hech qachon uchinchi shaxslarga "
            "oshkor qilinmaydi."
        ),
        "kaa": (
            "🏛 <b>Kásiplik Bilim Isenim Botı</b>\n\n"
            "Bul bot Qaraqalpaqstan Respublikasi Kásiplik bilimlendiriwdi "
            "rawajlandırıw basqarması tárepinen puqaralardan korrupciya "
            "jағdayları, usınıslar hám murájatlardı qabıl etiw maqsetinde "
            "jaratılgan.\n\n"
            "🔒 Anonim murájatlar tolıq sır saqlanadı. Sizdiń shaxsiy "
            "mағlıwmatlarıńız esh qashan úshinshi tárepke ashılmaydı."
        ),
        "ru": (
            "🏛 <b>Бот доверия профессионального образования</b>\n\n"
            "Этот бот создан Управлением развития профессионального "
            "образования Республики Каракалпакстан для приёма сообщений о "
            "коррупции, предложений и обращений граждан.\n\n"
            "🔒 Анонимные обращения хранятся в полной конфиденциальности. "
            "Ваши персональные данные никогда не передаются третьим лицам."
        ),
    },
    "contact_text": {
        "uz": "☎️ <b>Aloqa ma'lumotlari</b>",
        "kaa": "☎️ <b>Baylanıs mağlıwmatları</b>",
        "ru": "☎️ <b>Контактная информация</b>",
    },
    "back_to_menu": {
        "uz": "🔙 Bosh menyu",
        "kaa": "🔙 Бас меню",
        "ru": "🔙 Главное меню",
    },
    "unknown_command": {
        "uz": "Iltimos, menyudan mos tugmani tanlang.",
        "kaa": "Iltimas, menyuden sáykes túymeni tańlań.",
        "ru": "Пожалуйста, выберите пункт меню.",
    },
    "rate_limited": {
        "uz": "Iltimos, biroz kuting va qayta urinib ko'ring.",
        "kaa": "Iltimas, sәl kútip qayta urınıp kóriń.",
        "ru": "Пожалуйста, подождите немного и попробуйте снова.",
    },
    "file_too_large": {
        "uz": "Fayl hajmi juda katta. Maksimal hajm: {mb} MB.",
        "kaa": "Fayl kólemi tım úlken. Maksimal kólem: {mb} MB.",
        "ru": "Файл слишком большой. Максимальный размер: {mb} МБ.",
    },
    "admin_only": {
        "uz": "Bu buyruq faqat administrator uchun.",
        "kaa": "Bul buyrıq tek administrator ushın.",
        "ru": "Эта команда доступна только администратору.",
    },
    "reply_sent": {
        "uz": "Sizga administratordan javob keldi:\n\n{text}",
        "kaa": "Sizge administratordan juwap keldi:\n\n{text}",
        "ru": "Вам пришёл ответ от администратора:\n\n{text}",
    },
}


def labels(key: str) -> set[str]:
    """Return the set of localized button labels for `key` across all languages.

    Handy for matching a reply-keyboard button regardless of the user's
    current language, e.g. `F.text.in_(labels("menu_about"))`.
    """
    entry = TEXTS.get(key, {})
    return set(entry.values())


def t(key: str, lang: str, **kwargs: object) -> str:
    """Return the localized string for `key`/`lang`, formatted with kwargs."""
    entry = TEXTS.get(key)
    if entry is None:
        return key
    text = entry.get(lang) or entry.get("uz") or key
    if kwargs:
        return text.format(**kwargs)
    return text
