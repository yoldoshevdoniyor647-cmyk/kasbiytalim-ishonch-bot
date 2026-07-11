"""Input validation and sanitization helpers.

Raw user text is stored as-is in the database (trimmed/capped only). HTML
escaping is applied once, at the boundary where text is rendered into an
HTML-parse-mode Telegram message (see `services/notify.py` and
`handlers/admin.py`) — escaping at input time as well would double-escape
and corrupt the display (e.g. "&" becoming "&amp;amp;").
"""
from __future__ import annotations

import re

_PHONE_RE = re.compile(r"^\+?\d{7,15}$")


def is_valid_phone(phone: str) -> bool:
    """Loosely validate a phone number: optional '+' followed by 7-15 digits."""
    cleaned = phone.strip().replace(" ", "").replace("-", "")
    return bool(_PHONE_RE.match(cleaned))


def sanitize_text(text: str, max_length: int = 4000) -> str:
    """Trim whitespace and cap length to avoid oversized/abusive input."""
    return text.strip()[:max_length]


def validate_file_size(file_size: int | None, max_mb: int) -> bool:
    """Return True if the file size (bytes) is within the allowed limit."""
    if file_size is None:
        return True
    return file_size <= max_mb * 1024 * 1024
