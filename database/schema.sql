-- Schema for Kasbiy Ta'lim Ishonch Boti
-- SQLite database. All timestamps are stored as ISO-8601 UTC strings.

CREATE TABLE IF NOT EXISTS languages (
    code TEXT PRIMARY KEY,          -- 'uz' | 'kaa' | 'ru'
    name TEXT NOT NULL
);

INSERT OR IGNORE INTO languages (code, name) VALUES
    ('uz', "O'zbekcha"),
    ('kaa', 'Qaraqalpaqsha'),
    ('ru', 'Русский');

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL UNIQUE,
    username TEXT,
    full_name TEXT,
    language TEXT NOT NULL DEFAULT 'uz' REFERENCES languages(code),
    is_blocked INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_code TEXT NOT NULL UNIQUE,      -- e.g. CR-000001 / SG-000001
    user_id INTEGER NOT NULL REFERENCES users(id),
    kind TEXT NOT NULL,                    -- 'corruption' | 'suggestion'
    report_type TEXT,                      -- 'anonymous' | 'personal' (corruption only)
    full_name TEXT,
    phone TEXT,
    organization TEXT,
    district TEXT,
    message TEXT NOT NULL,
    language TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new',    -- 'new' | 'in_progress' | 'resolved' | 'rejected'
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    file_type TEXT NOT NULL,               -- 'photo' | 'video' | 'document' | 'voice'
    file_id TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,             -- YYYY-MM-DD
    new_users INTEGER NOT NULL DEFAULT 0,
    corruption_anonymous INTEGER NOT NULL DEFAULT 0,
    corruption_personal INTEGER NOT NULL DEFAULT 0,
    suggestions INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id);
CREATE INDEX IF NOT EXISTS idx_reports_created_at ON reports(created_at);
CREATE INDEX IF NOT EXISTS idx_attachments_report_id ON attachments(report_id);
