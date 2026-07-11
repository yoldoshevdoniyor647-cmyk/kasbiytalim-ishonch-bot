"""Database / CSV export helpers used by the admin panel."""
from __future__ import annotations

import csv
import io
from pathlib import Path

import aiofiles

from config import config
from database import fetch_all_reports

EXPORT_DIR = Path(__file__).parent.parent / "media" / "exports"

_CSV_COLUMNS = [
    "id",
    "report_code",
    "user_id",
    "kind",
    "report_type",
    "full_name",
    "phone",
    "organization",
    "district",
    "message",
    "language",
    "status",
    "created_at",
]


async def export_reports_csv() -> Path:
    """Write all reports to a CSV file under media/exports and return its path."""
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    rows = await fetch_all_reports()

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=_CSV_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

    file_path = EXPORT_DIR / "reports_export.csv"
    async with aiofiles.open(file_path, "w", encoding="utf-8-sig", newline="") as f:
        await f.write(buffer.getvalue())

    return file_path


def get_database_file_path() -> Path:
    """Return the path to the live SQLite database file for direct export."""
    return Path(config.database_path)
