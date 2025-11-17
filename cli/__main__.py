import typer

from cli.list_entries import aux_list_entries
from cli.log import aux_log
from cli.weekly_stats import aux_weekly_stats
from cli.mood_by_weather import aux_mood_by_weather

"""
This is the main hub for user commands
Actual functionalities are split across multiple modules
Each module is responsible for a single functionality
"""
app = typer.Typer(help="Mood & Weather Tracker CLI")



@app.command()
def list_entries():
    '''
    List all the entries
    '''
    aux_list_entries()


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

    aux_log(mood, note, city, lat, lng)
    

@app.command()
def weekly_stats():
    '''
    Retrieves average mood, average weather rating and average temperature on a weekly basis
    '''
    aux_weekly_stats()


@app.command()
def mood_by_weather():
    '''
    Retrieves average mood for each weather rating
    '''
    aux_mood_by_weather()

#Start the cli
if __name__ == "__main__":
    app()
