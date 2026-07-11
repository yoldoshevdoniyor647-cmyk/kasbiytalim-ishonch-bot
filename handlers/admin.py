"""Admin panel: statistics, exports, report search, replying to users and
changing report status. Every entry point is guarded by an ADMIN_ID check.
"""
from __future__ import annotations

from html import escape

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

import database
from config import config
from keyboards.inline import admin_back_keyboard, admin_menu_keyboard, status_choice_keyboard
from services.export import export_reports_csv, get_database_file_path
from states.states import AdminStates
from utils.logger import log_user_action
from utils.texts import t

router = Router(name="admin")


def _is_admin(telegram_id: int) -> bool:
    return telegram_id == config.admin_id


async def _stats_text() -> str:
    stats = await database.get_statistics()
    return (
        "📊 <b>Statistika</b>\n\n"
        f"👥 Foydalanuvchilar: {stats.total_users}\n"
        f"📅 Bugungi murojaatlar: {stats.reports_today}\n"
        f"🗂 Jami murojaatlar: {stats.reports_total}\n"
        f"🕵️ Anonim: {stats.anonymous_total}\n"
        f"🙋 Shaxsiy: {stats.personal_total}\n"
        f"💬 Takliflar: {stats.suggestions_total}"
    )


@router.message(Command("admin"))
async def open_admin_panel(message: Message, user_language: str) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer(t("admin_only", user_language))
        return
    await message.answer(await _stats_text(), reply_markup=admin_menu_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "admin:menu")
async def admin_menu_callback(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await callback.message.edit_text(
        await _stats_text(), reply_markup=admin_menu_keyboard(), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "admin:stats")
async def admin_stats_callback(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await callback.message.edit_text(
        await _stats_text(), reply_markup=admin_menu_keyboard(), parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "admin:export_db")
async def admin_export_db_callback(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    db_path = get_database_file_path()
    if db_path.exists():
        await callback.message.answer_document(FSInputFile(db_path, filename="database_export.db"))
    await callback.answer()


@router.callback_query(F.data == "admin:export_csv")
async def admin_export_csv_callback(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    csv_path = await export_reports_csv()
    await callback.message.answer_document(FSInputFile(csv_path, filename="reports_export.csv"))
    await callback.answer()


@router.callback_query(F.data == "admin:search")
async def admin_search_callback(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.set_state(AdminStates.waiting_search_code)
    await callback.message.answer("🔍 Murojaat ID sini kiriting (masalan: CR-000001):")
    await callback.answer()


@router.message(AdminStates.waiting_search_code, F.text)
async def admin_search_result(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    await state.clear()
    report = await database.get_report_by_code(message.text.strip().upper())
    if report is None:
        await message.answer("❌ Bunday ID li murojaat topilmadi.", reply_markup=admin_back_keyboard())
        return

    text = (
        f"🗂 <b>{report.report_code}</b>\n"
        f"Turi: {report.kind} / {report.report_type or '-'}\n"
        f"Holat: {report.status}\n"
        f"Til: {report.language}\n"
        f"Sana: {report.created_at}\n"
        f"F.I.Sh: {escape(report.full_name) if report.full_name else '—'}\n"
        f"Telefon: {escape(report.phone) if report.phone else '—'}\n"
        f"Tashkilot: {escape(report.organization) if report.organization else '—'}\n"
        f"Tuman: {escape(report.district) if report.district else '—'}\n\n"
        f"Xabar:\n{escape(report.message)}"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=status_choice_keyboard(report.report_code))


@router.callback_query(F.data.startswith("admin:setstatus:"))
async def admin_set_status_callback(callback: CallbackQuery) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    _, _, report_code, new_status = callback.data.split(":", maxsplit=3)
    updated = await database.update_report_status(report_code, new_status)
    if updated:
        await callback.answer("✅ Holat yangilandi")
        await callback.message.answer(f"Murojaat {report_code} holati '{new_status}' ga o'zgartirildi.")
    else:
        await callback.answer("❌ Xatolik", show_alert=True)


@router.callback_query(F.data == "admin:status")
async def admin_status_prompt_callback(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.set_state(AdminStates.waiting_status_code)
    await callback.message.answer("🔄 Holatini o'zgartirmoqchi bo'lgan murojaat ID sini kiriting:")
    await callback.answer()


@router.message(AdminStates.waiting_status_code, F.text)
async def admin_status_code_received(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    await state.clear()
    report_code = message.text.strip().upper()
    report = await database.get_report_by_code(report_code)
    if report is None:
        await message.answer("❌ Bunday ID li murojaat topilmadi.", reply_markup=admin_back_keyboard())
        return
    await message.answer(
        f"Murojaat {report_code} uchun yangi holatni tanlang:",
        reply_markup=status_choice_keyboard(report_code),
    )


@router.callback_query(F.data == "admin:reply")
async def admin_reply_prompt_callback(callback: CallbackQuery, state: FSMContext) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.set_state(AdminStates.waiting_reply_code)
    await callback.message.answer("✉️ Javob yubormoqchi bo'lgan murojaat ID sini kiriting:")
    await callback.answer()


@router.message(AdminStates.waiting_reply_code, F.text)
async def admin_reply_code_received(message: Message, state: FSMContext) -> None:
    if not _is_admin(message.from_user.id):
        return
    report_code = message.text.strip().upper()
    report = await database.get_report_by_code(report_code)
    if report is None:
        await message.answer("❌ Bunday ID li murojaat topilmadi.", reply_markup=admin_back_keyboard())
        await state.clear()
        return
    await state.update_data(reply_report_code=report_code)
    await state.set_state(AdminStates.waiting_reply_text)
    await message.answer("Javob matnini kiriting:")


@router.message(AdminStates.waiting_reply_text, F.text)
async def admin_reply_text_received(message: Message, state: FSMContext, bot: Bot) -> None:
    if not _is_admin(message.from_user.id):
        return
    data = await state.get_data()
    report_code = data.get("reply_report_code")
    await state.clear()

    report = await database.get_report_by_code(report_code)
    telegram_id = await database.get_user_telegram_id_for_report(report_code)

    if telegram_id is None or report is None:
        await message.answer("❌ Foydalanuvchi topilmadi.", reply_markup=admin_back_keyboard())
        return

    try:
        await bot.send_message(telegram_id, t("reply_sent", report.language, text=message.text))
        await message.answer(f"✅ Javob {report_code} murojaati egasiga yuborildi.")
        log_user_action(message.from_user.id, f"admin_reply_sent:{report_code}")
    except Exception:
        await message.answer("❌ Foydalanuvchiga xabar yuborib bo'lmadi (u botni bloklagan bo'lishi mumkin).")
