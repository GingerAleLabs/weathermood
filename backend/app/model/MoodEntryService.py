from model.db import get_connection
from datetime import datetime
from model.entities.MoodEntry import MoodEntry

class MoodEntryService:
    @staticmethod
    def add_entry(entry: MoodEntry):
        conn = get_connection()
        cur = conn.cursor()
        timestamp = datetime.now().isoformat()
        cur.execute(
            """
            INSERT INTO mood_entry (user_id, timestamp, mood, note, temperature, weather_rating)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (entry.user_id, timestamp, entry.mood, entry.note, entry.temperature, entry.weather_rating)
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
        return [MoodEntry(id=row['id'], user_id=row['user_id'], timestamp=row['timestamp'], mood=row['mood'], note=row['note'], temperature=row['temperature'], weather_rating=row['weather_rating']) for row in rows]