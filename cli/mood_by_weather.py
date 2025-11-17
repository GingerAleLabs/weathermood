import typer

from backend.app.services.StatsService import StatsService

from cli.utils import get_printable_rating

def aux_mood_by_weather():
    typer.echo("Mood by weather:")
    stats = StatsService.get_mood_per_weather_ranking()

    for ranking, s in stats.items():
        if s['num_entries'] == 0:
            typer.echo(f"{s['weather_description']}: No data")
        else:
            mood = get_printable_rating(round(s['avg_mood']))
            typer.echo(f"{s['weather_description']}: {mood} ({s['num_entries']} entries)")
        
        typer.echo('------------------------------------------------')