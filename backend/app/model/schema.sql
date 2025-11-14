CREATE TABLE IF NOT EXISTS mood_entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER, --for future extensions
    timestamp TEXT NOT NULL, --ISO-8601 string (eg 2025-01-10T14:30:00)
    mood INTEGER NOT NULL,
    note TEXT,
    temperature REAL NOT NULL,
    weather_rating INTEGER NOT NULL
);