"""Middleware that loads the current user's DB record/language into handler data."""
from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import database


class UserContextMiddleware(BaseMiddleware):
    """Injects `db_user` and `user_language` into handler data for every event.

    Defaults to 'uz' when the user has not completed language selection yet
    (e.g. their very first /start), so downstream handlers never need to
    guard against a missing language.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        db_user = None
        if user is not None:
            db_user = await database.get_user_by_telegram_id(user.id)

        data["db_user"] = db_user
        data["user_language"] = db_user.language if db_user else "uz"
        return await handler(event, data)
