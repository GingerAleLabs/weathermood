import typer

from backend.services.MoodEntryService import MoodEntryService
from backend.services.CityCoordsService import CityCoordsService
from backend.services.WeatherService import WeatherService

def aux_log(mood, note, city, lat, lng):
    '''
    validation rules:
        - either city or both lat/lng must be provided
        - if provided, -90 <= lat <= 90 and -180 <= lon <= 180
    '''
    latitude = lat
    longitude = lng

    if city is not None:
        if lat is not None or lng is not None:
            raise typer.BadParameter("You should only provide either a city name or its coordinates")
        else:
            #determine lat/lng from the city
            normalized_city = city.strip().lower().replace(" ", "_")
            cityCoords = CityCoordsService.getSupportedCitiesCoords()
            if(not normalized_city in cityCoords.keys()):
                raise typer.BadParameter(f"The city of {city} is not supported, please use its coordinates instead")
            else:
                coords = cityCoords[normalized_city]
                latitude  = coords['lat']
                longitude = coords['lng']
    else:
        #check that I have both lat and lng
        if lat is None and lng is None:
            raise typer.BadParameter(f"Please provide either a city name or its coordinates")
        elif lat is None or lng is None:
            raise typer.BadParameter(f"Please provide both latitude and longitude")
        elif not (-90 <= lat <= 90):
            raise typer.BadParameter(f"The latitude must be between -90 and 90")
        elif not (-180 <= lng <= 180):
            raise typer.BadParameter(f"The longitude must be between -180 and 180")

    #Here I'm sure that I have latitude/longitude and they are both valid

    weather = WeatherService.get_weather(latitude=latitude, longitude = longitude)
    temperature = weather['temperature']
    rating = weather['weather_rating']
    description = weather['weather_description']
    typer.echo(f"Current weather: {description}, {temperature} °C")

    MoodEntryService.add_entry(user_id=None, mood=mood, note=note, temperature=temperature, weather_rating=rating)
    typer.echo(f"Logged mood {mood} with note: '{note}'")