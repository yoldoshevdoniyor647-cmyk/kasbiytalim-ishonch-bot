"""Formats and forwards corruption/suggestion reports to the administrator."""
from __future__ import annotations

import datetime as dt
from html import escape
from typing import Optional

from aiogram import Bot
from aiogram.types import User

from config import config
from database import ReportRow, get_attachments

_SEPARATOR = "━━━━━━━━━━━━━━━"

_SEND_MAP = {
    "photo": "send_photo",
    "video": "send_video",
    "document": "send_document",
    "voice": "send_voice",
}

_ATTACHMENT_KWARG = {
    "photo": "photo",
    "video": "video",
    "document": "document",
    "voice": "voice",
}


def _field(value: Optional[str]) -> str:
    return escape(value) if value else "—"


def _build_report_text(report: ReportRow, tg_user: User) -> str:
    created = dt.datetime.fromisoformat(report.created_at)
    header = "🚨 NEW CORRUPTION REPORT" if report.kind == "corruption" else "💬 NEW SUGGESTION"
    type_label = {
        "anonymous": "Anonymous",
        "personal": "Personal",
    }.get(report.report_type or "", "Suggestion")

    lines = [
        _SEPARATOR,
        header,
        f"Report ID: {report.report_code}",
        f"Type: {type_label}",
        f"Date: {created:%Y-%m-%d}",
        f"Time: {created:%H:%M:%S}",
        f"Language: {report.language}",
        f"District: {_field(report.district)}",
        f"Organization: {_field(report.organization)}",
        f"User ID: {tg_user.id}",
        f"Username: {_field('@' + tg_user.username if tg_user.username else None)}",
        f"Full name: {_field(report.full_name)}",
        f"Phone: {_field(report.phone)}",
        "Text:",
        escape(report.message),
        _SEPARATOR,
    ]
    return "\n".join(lines)


async def notify_admin(bot: Bot, report: ReportRow, tg_user: User) -> None:
    """Send the formatted report and every attached media file to ADMIN_ID."""
    text = _build_report_text(report, tg_user)
    await bot.send_message(config.admin_id, text, parse_mode="HTML")

    attachments = await get_attachments(report.id)
    for attachment in attachments:
        method_name = _SEND_MAP.get(attachment["file_type"])
        if method_name is None:
            continue
        method = getattr(bot, method_name)
        kwarg = _ATTACHMENT_KWARG[attachment["file_type"]]
        await method(
            chat_id=config.admin_id,
            caption=f"{report.report_code} — {attachment['file_type']}",
            **{kwarg: attachment["file_id"]},
        )
