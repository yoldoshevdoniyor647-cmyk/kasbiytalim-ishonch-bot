"""/start command: greets new users with language selection, returning users
with the main menu in their saved language.
"""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import language_keyboard, main_menu_keyboard
from states.states import LanguageStates
from utils.logger import log_user_action
from utils.texts import t

router = Router(name="start")


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext, db_user) -> None:
    await state.clear()
    log_user_action(message.from_user.id, "start")

    if db_user is None:
        await message.answer(
            t("choose_language", "uz"), reply_markup=language_keyboard()
        )
        await state.set_state(LanguageStates.choosing)
        return

    await message.answer(
        t("welcome", db_user.language), reply_markup=main_menu_keyboard(db_user.language)
    )
