"""'ℹ️ Bot haqida' (About the bot) menu item."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import Message

from utils.logger import log_user_action
from utils.texts import labels, t

router = Router(name="about")


@router.message(F.text.in_(labels("menu_about")))
async def handle_about(message: Message, user_language: str) -> None:
    log_user_action(message.from_user.id, "view_about")
    await message.answer(t("about_text", user_language), parse_mode="HTML")
