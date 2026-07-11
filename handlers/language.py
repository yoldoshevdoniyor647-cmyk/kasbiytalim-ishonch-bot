"""Language selection: first-time onboarding and the 'change language' menu item."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import database
from keyboards.reply import language_keyboard, main_menu_keyboard
from states.states import LanguageStates
from utils.logger import log_user_action
from utils.texts import LANGUAGE_CODE_BY_NAME, labels, t

router = Router(name="language")


@router.message(F.text.in_(LANGUAGE_CODE_BY_NAME.keys()), LanguageStates.choosing)
async def handle_language_choice(message: Message, state: FSMContext, db_user) -> None:
    lang = LANGUAGE_CODE_BY_NAME[message.text]

    if db_user is None:
        db_user = await database.create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
            language=lang,
        )
        welcome_text = t("welcome", lang)
    else:
        await database.set_user_language(message.from_user.id, lang)
        welcome_text = t("language_changed", lang)

    log_user_action(message.from_user.id, f"language_set:{lang}")
    await state.clear()
    await message.answer(welcome_text, reply_markup=main_menu_keyboard(lang))


@router.message(F.text.in_(labels("menu_language")))
async def handle_change_language_request(message: Message, state: FSMContext, user_language: str) -> None:
    await state.set_state(LanguageStates.choosing)
    await message.answer(t("choose_language", user_language), reply_markup=language_keyboard())
