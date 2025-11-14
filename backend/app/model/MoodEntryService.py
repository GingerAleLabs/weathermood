from model.db import get_connection
from datetime import datetime

class MoodEntryService:
    @staticmethod
    def add_entry(
        mood: int, note: str | None, temperature: float, weather_rating: int, user_id: int | None = None):
        conn = get_connection()
        cur = conn.cursor()
        timestamp = datetime.now().isoformat()
        cur.execute(
            """
            INSERT INTO mood_entry (user_id, timestamp, mood, note, temperature, weather_rating)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, timestamp, mood, note, temperature, weather_rating)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_entries():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mood_entry ORDER BY timestamp DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]