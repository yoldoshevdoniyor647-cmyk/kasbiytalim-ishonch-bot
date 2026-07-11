"""Async SQLite data access layer built on top of aiosqlite.

A single module-level connection pool is not used on purpose (SQLite is
file-based); instead every call opens a short-lived connection via
`aiosqlite.connect`, which is cheap and keeps the code simple and safe for
concurrent asyncio tasks.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import aiosqlite

from config import config

SCHEMA_PATH = Path(__file__).parent / "database" / "schema.sql"


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


async def init_db() -> None:
    """Create tables if they do not exist yet. Safe to call on every startup."""
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    async with aiosqlite.connect(config.database_path) as db:
        await db.executescript(schema)
        await db.commit()


# --------------------------------------------------------------------------
# Users
# --------------------------------------------------------------------------

@dataclass
class UserRow:
    id: int
    telegram_id: int
    username: Optional[str]
    full_name: Optional[str]
    language: str
    is_blocked: bool
    created_at: str


async def get_user_by_telegram_id(telegram_id: int) -> Optional[UserRow]:
    async with aiosqlite.connect(config.database_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        )
        row = await cursor.fetchone()
        if row is None:
            return None
        return UserRow(
            id=row["id"],
            telegram_id=row["telegram_id"],
            username=row["username"],
            full_name=row["full_name"],
            language=row["language"],
            is_blocked=bool(row["is_blocked"]),
            created_at=row["created_at"],
        )


async def create_user(
    telegram_id: int, username: Optional[str], full_name: Optional[str], language: str
) -> UserRow:
    async with aiosqlite.connect(config.database_path) as db:
        await db.execute(
            """INSERT INTO users (telegram_id, username, full_name, language, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (telegram_id, username, full_name, language, _now()),
        )
        await db.commit()
    await _bump_statistic("new_users")
    user = await get_user_by_telegram_id(telegram_id)
    assert user is not None
    return user


async def set_user_language(telegram_id: int, language: str) -> None:
    async with aiosqlite.connect(config.database_path) as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE telegram_id = ?",
            (language, telegram_id),
        )
        await db.commit()


async def count_users() -> int:
    async with aiosqlite.connect(config.database_path) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        (count,) = await cursor.fetchone()
        return count


# --------------------------------------------------------------------------
# Reports (corruption reports + suggestions share one table, `kind` field)
# --------------------------------------------------------------------------

@dataclass
class ReportRow:
    id: int
    report_code: str
    user_id: int
    kind: str
    report_type: Optional[str]
    full_name: Optional[str]
    phone: Optional[str]
    organization: Optional[str]
    district: Optional[str]
    message: str
    language: str
    status: str
    created_at: str


def _row_to_report(row: aiosqlite.Row) -> ReportRow:
    return ReportRow(
        id=row["id"],
        report_code=row["report_code"],
        user_id=row["user_id"],
        kind=row["kind"],
        report_type=row["report_type"],
        full_name=row["full_name"],
        phone=row["phone"],
        organization=row["organization"],
        district=row["district"],
        message=row["message"],
        language=row["language"],
        status=row["status"],
        created_at=row["created_at"],
    )


async def _next_report_code(kind: str) -> str:
    prefix = "CR" if kind == "corruption" else "SG"
    async with aiosqlite.connect(config.database_path) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM reports WHERE kind = ?", (kind,)
        )
        (count,) = await cursor.fetchone()
    return f"{prefix}-{count + 1:06d}"


async def create_report(
    user_id: int,
    kind: str,
    message: str,
    language: str,
    report_type: Optional[str] = None,
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
    organization: Optional[str] = None,
    district: Optional[str] = None,
) -> ReportRow:
    report_code = await _next_report_code(kind)
    async with aiosqlite.connect(config.database_path) as db:
        cursor = await db.execute(
            """INSERT INTO reports
               (report_code, user_id, kind, report_type, full_name, phone,
                organization, district, message, language, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'new', ?)""",
            (
                report_code,
                user_id,
                kind,
                report_type,
                full_name,
                phone,
                organization,
                district,
                message,
                language,
                _now(),
            ),
        )
        await db.commit()
        report_id = cursor.lastrowid

    if kind == "corruption" and report_type == "anonymous":
        await _bump_statistic("corruption_anonymous")
    elif kind == "corruption" and report_type == "personal":
        await _bump_statistic("corruption_personal")
    elif kind == "suggestion":
        await _bump_statistic("suggestions")

    async with aiosqlite.connect(config.database_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
        row = await cursor.fetchone()
    assert row is not None
    return _row_to_report(row)


async def add_attachment(report_id: int, file_type: str, file_id: str) -> None:
    async with aiosqlite.connect(config.database_path) as db:
        await db.execute(
            """INSERT INTO attachments (report_id, file_type, file_id, created_at)
               VALUES (?, ?, ?, ?)""",
            (report_id, file_type, file_id, _now()),
        )
        await db.commit()


async def get_attachments(report_id: int) -> list[aiosqlite.Row]:
    async with aiosqlite.connect(config.database_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM attachments WHERE report_id = ?", (report_id,)
        )
        return list(await cursor.fetchall())


async def get_report_by_code(report_code: str) -> Optional[ReportRow]:
    async with aiosqlite.connect(config.database_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM reports WHERE report_code = ?", (report_code,)
        )
        row = await cursor.fetchone()
        return _row_to_report(row) if row else None


async def update_report_status(report_code: str, status: str) -> bool:
    async with aiosqlite.connect(config.database_path) as db:
        cursor = await db.execute(
            "UPDATE reports SET status = ? WHERE report_code = ?",
            (status, report_code),
        )
        await db.commit()
        return cursor.rowcount > 0


async def get_user_telegram_id_for_report(report_code: str) -> Optional[int]:
    async with aiosqlite.connect(config.database_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """SELECT u.telegram_id FROM users u
               JOIN reports r ON r.user_id = u.id
               WHERE r.report_code = ?""",
            (report_code,),
        )
        row = await cursor.fetchone()
        return row["telegram_id"] if row else None


# --------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------

async def _bump_statistic(column: str) -> None:
    today = dt.date.today().isoformat()
    async with aiosqlite.connect(config.database_path) as db:
        await db.execute(
            "INSERT OR IGNORE INTO statistics (date) VALUES (?)", (today,)
        )
        await db.execute(
            f"UPDATE statistics SET {column} = {column} + 1 WHERE date = ?",
            (today,),
        )
        await db.commit()


@dataclass
class Stats:
    total_users: int
    reports_today: int
    reports_total: int
    anonymous_total: int
    personal_total: int
    suggestions_total: int


async def get_statistics() -> Stats:
    today = dt.date.today().isoformat()
    async with aiosqlite.connect(config.database_path) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("SELECT COUNT(*) AS c FROM users")
        total_users = (await cursor.fetchone())["c"]

        cursor = await db.execute(
            "SELECT COUNT(*) AS c FROM reports WHERE date(created_at) = ?", (today,)
        )
        reports_today = (await cursor.fetchone())["c"]

        cursor = await db.execute("SELECT COUNT(*) AS c FROM reports")
        reports_total = (await cursor.fetchone())["c"]

        cursor = await db.execute(
            "SELECT COUNT(*) AS c FROM reports WHERE report_type = 'anonymous'"
        )
        anonymous_total = (await cursor.fetchone())["c"]

        cursor = await db.execute(
            "SELECT COUNT(*) AS c FROM reports WHERE report_type = 'personal'"
        )
        personal_total = (await cursor.fetchone())["c"]

        cursor = await db.execute(
            "SELECT COUNT(*) AS c FROM reports WHERE kind = 'suggestion'"
        )
        suggestions_total = (await cursor.fetchone())["c"]

    return Stats(
        total_users=total_users,
        reports_today=reports_today,
        reports_total=reports_total,
        anonymous_total=anonymous_total,
        personal_total=personal_total,
        suggestions_total=suggestions_total,
    )


async def fetch_all_reports() -> list[dict[str, Any]]:
    """Return every report row as a plain dict, used for CSV export."""
    async with aiosqlite.connect(config.database_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM reports ORDER BY id")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
