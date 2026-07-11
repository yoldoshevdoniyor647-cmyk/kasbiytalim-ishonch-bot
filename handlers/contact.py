"""'☎️ Aloqa' (Contact) menu item."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.types import Message

from config import config
from utils.logger import log_user_action
from utils.texts import labels, t

router = Router(name="contact")


@router.message(F.text.in_(labels("menu_contact")))
async def handle_contact(message: Message, user_language: str) -> None:
    log_user_action(message.from_user.id, "view_contact")
    contact = config.contact

    lines = [t("contact_text", user_language), ""]
    if contact.phone:
        lines.append(f"☎️ {contact.phone}")
    if contact.email:
        lines.append(f"📧 {contact.email}")
    if contact.website:
        lines.append(f"🌐 {contact.website}")
    if contact.address:
        lines.append(f"📍 {contact.address}")

    await message.answer("\n".join(lines), parse_mode="HTML")

    if contact.latitude and contact.longitude:
        await message.answer_location(latitude=contact.latitude, longitude=contact.longitude)
