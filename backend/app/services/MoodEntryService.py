from backend.app.model.db import get_connection
from datetime import datetime
from backend.app.domain.weather_scale import get_weather_description

class MoodEntryService:


    #Add an entry

    @staticmethod
    def add_entry(user_id:int | None, mood, note, temperature, weather_rating):
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


    #Retrieve all entries

    @staticmethod
    def get_entries():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT timestamp, mood, note, temperature, weather_rating 
            FROM mood_entry 
            ORDER BY timestamp DESC
            """
        )
        rows = cur.fetchall()
        conn.close()

        entries = [
            {
                'timestamp':row['timestamp'], 
                'mood':row['mood'], 
                'note':row['note'], 
                'temperature':row['temperature'], 
                'weather_rating':row['weather_rating'], 
                'weather_description':get_weather_description(row['weather_rating']),
            } 
            for row in rows
        ]

        return entries