"""Full corruption-report FSM flow: anonymous or personal, multi-file evidence,
confirmation and admin forwarding.
"""
from __future__ import annotations

from typing import Any

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import database
from config import config
from keyboards.reply import (
    confirm_keyboard,
    evidence_keyboard,
    main_menu_keyboard,
    report_type_keyboard,
)
from services.notify import notify_admin
from states.states import CorruptionReportStates
from utils.logger import log_user_action
from utils.texts import labels, t
from utils.validators import is_valid_phone, sanitize_text, validate_file_size

router = Router(name="corruption")

_EVIDENCE_HINT_LABELS = (
    labels("btn_photo") | labels("btn_video") | labels("btn_document") | labels("btn_voice")
)


@router.message(F.text.in_(labels("menu_corruption")))
async def start_corruption_report(message: Message, state: FSMContext, user_language: str) -> None:
    log_user_action(message.from_user.id, "corruption_flow_start")
    await state.clear()
    await state.set_data({"attachments": []})
    await state.set_state(CorruptionReportStates.choosing_type)
    await message.answer(
        t("choose_report_type", user_language), reply_markup=report_type_keyboard(user_language)
    )


@router.message(CorruptionReportStates.choosing_type, F.text.in_(labels("btn_anonymous")))
async def choose_anonymous(message: Message, state: FSMContext, user_language: str) -> None:
    await state.update_data(report_type="anonymous")
    await state.set_state(CorruptionReportStates.waiting_message)
    await message.answer(t("ask_report_text", user_language))


@router.message(CorruptionReportStates.choosing_type, F.text.in_(labels("btn_personal")))
async def choose_personal(message: Message, state: FSMContext, user_language: str) -> None:
    await state.update_data(report_type="personal")
    await state.set_state(CorruptionReportStates.waiting_full_name)
    await message.answer(t("ask_full_name", user_language))


@router.message(CorruptionReportStates.waiting_full_name, F.text)
async def receive_full_name(message: Message, state: FSMContext, user_language: str) -> None:
    await state.update_data(full_name=sanitize_text(message.text, max_length=200))
    await state.set_state(CorruptionReportStates.waiting_phone)
    await message.answer(t("ask_phone", user_language))


@router.message(CorruptionReportStates.waiting_phone, F.text)
async def receive_phone(message: Message, state: FSMContext, user_language: str) -> None:
    if not is_valid_phone(message.text):
        await message.answer(t("invalid_phone", user_language))
        return
    await state.update_data(phone=message.text.strip())
    await state.set_state(CorruptionReportStates.waiting_organization)
    await message.answer(t("ask_organization", user_language))


@router.message(CorruptionReportStates.waiting_organization, F.text)
async def receive_organization(message: Message, state: FSMContext, user_language: str) -> None:
    await state.update_data(organization=sanitize_text(message.text, max_length=200))
    await state.set_state(CorruptionReportStates.waiting_district)
    await message.answer(t("ask_district", user_language))


@router.message(CorruptionReportStates.waiting_district, F.text)
async def receive_district(message: Message, state: FSMContext, user_language: str) -> None:
    await state.update_data(district=sanitize_text(message.text, max_length=200))
    await state.set_state(CorruptionReportStates.waiting_message)
    await message.answer(t("ask_report_text", user_language))


@router.message(CorruptionReportStates.waiting_message, F.text)
async def receive_message_text(message: Message, state: FSMContext, user_language: str) -> None:
    await state.update_data(message_text=sanitize_text(message.text))
    await state.set_state(CorruptionReportStates.waiting_evidence)
    await message.answer(t("ask_evidence", user_language), reply_markup=evidence_keyboard(user_language))


async def _store_attachment(
    state: FSMContext, message: Message, user_language: str, file_type: str, file_id: str, file_size: int | None
) -> None:
    if not validate_file_size(file_size, config.max_upload_mb):
        await message.answer(t("file_too_large", user_language, mb=config.max_upload_mb))
        return
    data = await state.get_data()
    attachments: list[dict[str, str]] = data.get("attachments", [])
    attachments.append({"file_type": file_type, "file_id": file_id})
    await state.update_data(attachments=attachments)
    await message.answer(t("evidence_received", user_language), reply_markup=evidence_keyboard(user_language))


@router.message(CorruptionReportStates.waiting_evidence, F.photo)
async def receive_photo(message: Message, state: FSMContext, user_language: str) -> None:
    photo = message.photo[-1]
    await _store_attachment(state, message, user_language, "photo", photo.file_id, photo.file_size)


@router.message(CorruptionReportStates.waiting_evidence, F.video)
async def receive_video(message: Message, state: FSMContext, user_language: str) -> None:
    video = message.video
    await _store_attachment(state, message, user_language, "video", video.file_id, video.file_size)


@router.message(CorruptionReportStates.waiting_evidence, F.document)
async def receive_document(message: Message, state: FSMContext, user_language: str) -> None:
    document = message.document
    await _store_attachment(state, message, user_language, "document", document.file_id, document.file_size)


@router.message(CorruptionReportStates.waiting_evidence, F.voice)
async def receive_voice(message: Message, state: FSMContext, user_language: str) -> None:
    voice = message.voice
    await _store_attachment(state, message, user_language, "voice", voice.file_id, voice.file_size)


@router.message(CorruptionReportStates.waiting_evidence, F.text.in_(_EVIDENCE_HINT_LABELS))
async def evidence_hint(message: Message, user_language: str) -> None:
    await message.answer(t("ask_evidence", user_language), reply_markup=evidence_keyboard(user_language))


@router.message(CorruptionReportStates.waiting_evidence, F.text.in_(labels("btn_skip")))
async def finish_evidence(message: Message, state: FSMContext, user_language: str) -> None:
    await state.set_state(CorruptionReportStates.confirming)
    await message.answer(t("ask_send_confirm", user_language), reply_markup=confirm_keyboard(user_language))


@router.message(CorruptionReportStates.confirming, F.text.in_(labels("btn_cancel")))
async def cancel_report(message: Message, state: FSMContext, user_language: str) -> None:
    log_user_action(message.from_user.id, "corruption_report_cancelled")
    await state.clear()
    await message.answer(t("report_cancelled", user_language), reply_markup=main_menu_keyboard(user_language))


@router.message(CorruptionReportStates.confirming, F.text.in_(labels("btn_send")))
async def send_report(message: Message, state: FSMContext, user_language: str, bot: Bot) -> None:
    data: dict[str, Any] = await state.get_data()

    db_user = await database.get_user_by_telegram_id(message.from_user.id)
    if db_user is None:
        db_user = await database.create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
            language=user_language,
        )

    report = await database.create_report(
        user_id=db_user.id,
        kind="corruption",
        message=data.get("message_text", ""),
        language=user_language,
        report_type=data.get("report_type", "anonymous"),
        full_name=data.get("full_name"),
        phone=data.get("phone"),
        organization=data.get("organization"),
        district=data.get("district"),
    )

    for attachment in data.get("attachments", []):
        await database.add_attachment(report.id, attachment["file_type"], attachment["file_id"])

    await notify_admin(bot, report, message.from_user)

    log_user_action(message.from_user.id, f"corruption_report_sent:{report.report_code}")
    await state.clear()
    await message.answer(
        t("report_sent", user_language, code=report.report_code),
        reply_markup=main_menu_keyboard(user_language),
    )
