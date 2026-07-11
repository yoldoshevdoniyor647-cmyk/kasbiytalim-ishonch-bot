"""Application-wide logging configuration.

Two rotating log files are produced under `logs/`:
  - `logs/bot.log`    general info / user actions
  - `logs/errors.log` warnings and above
"""
from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent / "logs"


def setup_logging() -> None:
    LOGS_DIR.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    info_handler = RotatingFileHandler(
        LOGS_DIR / "bot.log", maxBytes=5_000_000, backupCount=3, encoding="utf-8"
    )
    info_handler.setFormatter(formatter)
    info_handler.setLevel(logging.INFO)

    error_handler = RotatingFileHandler(
        LOGS_DIR / "errors.log", maxBytes=5_000_000, backupCount=3, encoding="utf-8"
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.WARNING)

    root.handlers.clear()
    root.addHandler(console_handler)
    root.addHandler(info_handler)
    root.addHandler(error_handler)

    # aiogram/aiohttp are noisy on INFO; keep them at WARNING.
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)


action_logger = logging.getLogger("user_actions")


def log_user_action(telegram_id: int, action: str) -> None:
    action_logger.info("user=%s action=%s", telegram_id, action)
