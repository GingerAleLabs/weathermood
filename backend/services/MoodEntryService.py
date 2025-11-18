from backend.model.DbException import DbException
from backend.model.db import get_connection
from datetime import datetime
from backend.domain.weather_scale import get_weather_description
from backend.services.ServiceUnavailableException import ServiceUnavailableException

class MoodEntryService:


    # Add an entry
    # mood : int (1-5)
    # weather-rating : int (1-5)
    @staticmethod
    def add_entry(user_id:int | None, mood, note, temperature, weather_rating):
        if temperature is None:
            raise TypeError("Temperature cannot be None")
        if mood is None:
            raise TypeError("Mood cannot be None")
        if weather_rating is None:
            raise TypeError("Weather rating cannot be None")
        if not (1 <= mood <= 5):
            raise ValueError("Mood must be between 1 and 5")
        if not (1 <= weather_rating <= 5):
            raise ValueError("Weather rating must be between 1 and 5")
        
        try:
            with get_connection() as conn:
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
        except DbException as e:
            raise ServiceUnavailableException("Could not add mood entry") from e


    #Retrieve all entries

    @staticmethod
    def get_entries():
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT timestamp, mood, note, temperature, weather_rating 
                    FROM mood_entry 
                    ORDER BY timestamp DESC
                    """
                )
                rows = cur.fetchall()

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
        except (DbException, KeyError) as e:
            raise ServiceUnavailableException("Could not retrieve the entries") from e