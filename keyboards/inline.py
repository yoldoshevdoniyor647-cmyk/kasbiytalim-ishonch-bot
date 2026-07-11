"""Inline keyboards, mainly for the admin panel."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin:stats")],
        [
            InlineKeyboardButton(text="📁 Export DB", callback_data="admin:export_db"),
            InlineKeyboardButton(text="📄 Export CSV", callback_data="admin:export_csv"),
        ],
        [InlineKeyboardButton(text="🔍 ID bo'yicha qidirish", callback_data="admin:search")],
        [InlineKeyboardButton(text="✉️ Foydalanuvchiga javob", callback_data="admin:reply")],
        [InlineKeyboardButton(text="🔄 Status o'zgartirish", callback_data="admin:status")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def status_choice_keyboard(report_code: str) -> InlineKeyboardMarkup:
    statuses = [
        ("🆕 Yangi", "new"),
        ("⏳ Jarayonda", "in_progress"),
        ("✅ Hal qilindi", "resolved"),
        ("❌ Rad etildi", "rejected"),
    ]
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"admin:setstatus:{report_code}:{value}")]
        for label, value in statuses
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Admin menyu", callback_data="admin:menu")]]
    )
