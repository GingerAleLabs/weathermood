import typer
from model.MoodEntryService import MoodEntryService
from model.db import init_db
from domain.city_coords import CITY_COORDS

# db initialization
init_db()



"""
CLI COMMANDS
"""
app = typer.Typer(help="Mood & Weather Tracker CLI")


# List all the entries
@app.command()
def list_entries():
    entries = MoodEntryService.get_entries()
    if not entries:
        typer.echo("No entries found.")
        return

    for e in entries:
        ts = e["timestamp"]
        typer.echo(f"{ts} | Mood: {e['mood']} | Weather: {e['weather_rating']} | Note: {e['note']}")


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
            if(not normalized_city in CITY_COORDS.keys()):
                raise typer.BadParameter(f"The city of {city} is not supported, please use its coordinates instead")
            else:
                coords = CITY_COORDS[normalized_city]
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
        elif not (-180 <= lon <= 180):
            raise typer.BadParameter(f"The longitude must be between -180 and 180")

    #Here I'm sure that I have latitude/longitude and they are both valid
    typer.echo(f"Lat: {latitude}, lng: '{longitude}'")

    #TODO meteo api
    temperature = 20
    weather_rating = 3

    MoodEntryService.add_entry(mood, note, temperature, weather_rating)
    typer.echo(f"Logged mood {mood} with note: '{note}'")



# List all entries
@app.command()
def list_entries():
    entries = MoodEntryService.get_entries()
    for e in entries:
        print(e)

#Start the cli
if __name__ == "__main__":
    app()
