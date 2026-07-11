"""FSM state groups for all multi-step conversations."""
from aiogram.fsm.state import State, StatesGroup


class LanguageStates(StatesGroup):
    choosing = State()


class CorruptionReportStates(StatesGroup):
    choosing_type = State()
    waiting_full_name = State()
    waiting_phone = State()
    waiting_organization = State()
    waiting_district = State()
    waiting_message = State()
    waiting_evidence = State()
    confirming = State()


class SuggestionStates(StatesGroup):
    waiting_message = State()
    waiting_evidence = State()
    confirming = State()


class AdminStates(StatesGroup):
    waiting_search_code = State()
    waiting_reply_code = State()
    waiting_reply_text = State()
    waiting_status_code = State()
