from backend.model.DbException import DbException
from backend.model.db_queries import add_entry as db_queries_add_entry
from backend.model.db_queries import get_entries as db_queries_get_entries

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
            db_queries_add_entry(user_id, mood, note, temperature, weather_rating)
        except DbException as e:
            raise ServiceUnavailableException("Could not add mood entry") from e


    #Retrieve all entries
    @staticmethod
    def get_entries():
        try:
            entries = db_queries_get_entries()
            return [
                {
                    **entry, 
                    "weather_description": get_weather_description(entry["weather_rating"])
                }
                for entry in entries
            ]
        except (DbException) as e:
            raise ServiceUnavailableException("Could not retrieve the entries") from e