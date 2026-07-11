"""Entry point for Kasbiy Ta'lim Ishonch Boti (@kasbiytalim_ishonch_qqr_bot).

Runs the bot in long-polling mode. Suitable for a Render.com Background
Worker (see render.yaml) or for local development.
"""
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from database import init_db
from handlers import about, admin, contact, corruption, language, menu, start, suggestion
from utils.logger import setup_logging
from utils.middlewares import UserContextMiddleware
from utils.throttling import ThrottlingMiddleware

logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logging()
    await init_db()
    logger.info("Database initialized at %s", config.database_path)

    # No default parse_mode: most messages are plain user/admin text and must
    # not be run through Telegram's HTML entity parser. Screens that embed our
    # own markup (about/contact/stats/admin report view) pass parse_mode="HTML"
    # explicitly and escape any interpolated user data themselves.
    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    # Order matters: UserContextMiddleware must run before ThrottlingMiddleware
    # so the rate-limit notice can be sent in the user's own language.
    for observer in (dp.message, dp.callback_query):
        observer.middleware(UserContextMiddleware())
        observer.middleware(ThrottlingMiddleware(config.rate_limit_seconds))

    # `menu` is registered last: it contains the catch-all fallback handler
    # that must only fire when no other, more specific handler matched.
    dp.include_routers(
        start.router,
        language.router,
        admin.router,
        corruption.router,
        suggestion.router,
        about.router,
        contact.router,
        menu.router,
    )

    logger.info("Starting bot polling...")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.getLogger(__name__).info("Bot stopped.")
