"""Application configuration loaded from environment variables.

All secrets (bot token, admin id) must never be hardcoded. They are read
from a `.env` file in development and from the platform's environment
variables (e.g. Render dashboard) in production.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Environment variable '{name}' is required but not set. "
            f"Copy .env.example to .env and fill it in."
        )
    return value


@dataclass(frozen=True)
class ContactInfo:
    phone: str = field(default_factory=lambda: os.getenv("CONTACT_PHONE", "+998 91 304 00 09"))
    email: str = field(default_factory=lambda: os.getenv("CONTACT_EMAIL", ""))
    website: str = field(default_factory=lambda: os.getenv("CONTACT_WEBSITE", ""))
    address: str = field(default_factory=lambda: os.getenv("CONTACT_ADDRESS", ""))
    latitude: float = field(default_factory=lambda: float(os.getenv("CONTACT_LATITUDE", "0") or 0))
    longitude: float = field(default_factory=lambda: float(os.getenv("CONTACT_LONGITUDE", "0") or 0))


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_id: int
    database_path: str
    max_upload_mb: int
    rate_limit_seconds: float
    contact: ContactInfo


def load_config() -> Config:
    """Build and return the immutable application configuration."""
    return Config(
        bot_token=_require("BOT_TOKEN"),
        admin_id=int(_require("ADMIN_ID")),
        database_path=os.getenv("DATABASE", "database.db"),
        max_upload_mb=int(os.getenv("MAX_UPLOAD_MB", "20")),
        rate_limit_seconds=float(os.getenv("RATE_LIMIT_SECONDS", "1.5")),
        contact=ContactInfo(),
    )


config = load_config()
