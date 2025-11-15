import typer
from datetime import datetime

from backend.app.services.MoodEntryService import MoodEntryService
from backend.app.services.CityCoordsService import CityCoordsService
from backend.app.services.WeatherService import WeatherService


"""
CLI COMMANDS
"""
app = typer.Typer(help="Mood & Weather Tracker CLI")


def print_entry(entry):
    stars=['*----', '**---', '***--', '****-', '*****']
    dt = datetime.fromisoformat(entry['timestamp'])
    typer.echo(dt.strftime("%A, %d %B %Y %H:%M"))
    typer.echo(f"Mood: {stars[entry['mood']-1]}")
    typer.echo(f"Weather: {entry['weather_description']}, {entry['temperature']}°C")
    if not (entry['note']==""):
        typer.echo(f">> {entry['note']}")
    typer.echo('------------------------------------------------')

@app.command()
def list_entries():
    '''
    List all the entries
    '''
    entries = MoodEntryService.get_entries()

    if not entries:
        typer.echo("No entries found.")
        return

    for e in entries:
        print_entry(e)


# Log a new entry
@app.command()
def log(
        mood: int = typer.Option(..., "-mood", help="Your mood rating from 1 to 5", min=1, max=5),
        note: str = typer.Option("", "-note", help="Optional note about your mood"),
        city: str = typer.Option(None, "-city", help="City name (optional)"),
        lat: float = typer.Option(None, "-lat", help="Latitude (optional)"),
        lng: float = typer.Option(None, "-lng", help="Longitude (optional)"),
    ): 
    '''
    Log an entry providing the mood rating(1-5), an optional note, and a city or coordinates
    '''
    
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
    typer.echo(f"Temperature {temperature}, rating: {rating} {description}")

    MoodEntryService.add_entry(user_id=None, mood=mood, note=note, temperature=temperature, weather_rating=rating)
    typer.echo(f"Logged mood {mood} with note: '{note}'")


#Start the cli
if __name__ == "__main__":
    app()
