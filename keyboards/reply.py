"""Reply (persistent) keyboards."""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from utils.texts import LANGUAGE_NAMES, t


def language_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard shown on first /start, one button per supported language."""
    buttons = [[KeyboardButton(text=name)] for name in LANGUAGE_NAMES.values()]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Main menu shown after language selection / '/start'."""
    keyboard = [
        [KeyboardButton(text=t("menu_corruption", lang))],
        [KeyboardButton(text=t("menu_suggestion", lang))],
        [KeyboardButton(text=t("menu_contact", lang)), KeyboardButton(text=t("menu_about", lang))],
        [KeyboardButton(text=t("menu_language", lang))],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def report_type_keyboard(lang: str) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=t("btn_anonymous", lang))],
        [KeyboardButton(text=t("btn_personal", lang))],
        [KeyboardButton(text=t("back_to_menu", lang))],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def evidence_keyboard(lang: str) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=t("btn_photo", lang)), KeyboardButton(text=t("btn_video", lang))],
        [KeyboardButton(text=t("btn_document", lang)), KeyboardButton(text=t("btn_voice", lang))],
        [KeyboardButton(text=t("btn_skip", lang))],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def confirm_keyboard(lang: str) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=t("btn_send", lang)), KeyboardButton(text=t("btn_cancel", lang))],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
