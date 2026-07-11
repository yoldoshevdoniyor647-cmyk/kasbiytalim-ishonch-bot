"""Main-menu navigation: 'back to menu' button and the final catch-all fallback.

The fallback handler in this router must be included LAST in bot.py so every
more specific handler gets a chance to match first.
"""
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import main_menu_keyboard
from utils.texts import labels, t

router = Router(name="menu")


@router.message(F.text.in_(labels("back_to_menu")))
async def handle_back_to_menu(message: Message, state: FSMContext, user_language: str) -> None:
    await state.clear()
    await message.answer(t("welcome", user_language), reply_markup=main_menu_keyboard(user_language))


@router.message()
async def handle_unknown(message: Message, user_language: str) -> None:
    await message.answer(t("unknown_command", user_language), reply_markup=main_menu_keyboard(user_language))
