"""Simple in-memory rate-limiting (anti-spam) middleware."""
from __future__ import annotations

import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from utils.texts import t


class ThrottlingMiddleware(BaseMiddleware):
    """Drops events that arrive faster than `rate_limit_seconds` per user.

    Registered separately on `dp.message` and `dp.callback_query`, so `event`
    is always a `Message` or `CallbackQuery`, never a raw `Update`.
    A lightweight alternative to a Redis-backed limiter, sufficient for a
    single-instance deployment such as Render's free/starter tier.
    """

    def __init__(self, rate_limit_seconds: float) -> None:
        self.rate_limit_seconds = rate_limit_seconds
        self._last_seen: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        now = time.monotonic()
        last = self._last_seen.get(user.id)
        self._last_seen[user.id] = now

        if last is not None and (now - last) < self.rate_limit_seconds:
            lang = data.get("user_language", "uz")
            answerable = getattr(event, "message", event)
            try:
                await answerable.answer(t("rate_limited", lang))
            except Exception:
                pass
            return None

        return await handler(event, data)
