import requests
from backend.domain.weather_scale import get_weather_description, convert_openmeteo_rating

class WeatherService:

    @staticmethod
    def get_weather(latitude: float, longitude: float):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # raises an error if request failed
        data = response.json()

        temperature = data["current_weather"]["temperature"]
        open_meteo_rating = data["current_weather"]["weathercode"]

        weather_rating = convert_openmeteo_rating(open_meteo_rating)
        weather_description = get_weather_description(weather_rating)

        res = {
            'temperature': temperature,
            'weather_rating': weather_rating,
            'weather_description': weather_description
        }

        return res