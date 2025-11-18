import typer

from backend.services import ServiceUnavailableException
from backend.services.StatsService import StatsService

from cli.utils import get_printable_rating
from datetime import date

def aux_weekly_stats():
    try:
        typer.echo("weekly stats:")
        stats = StatsService.get_weekly_stats()

        for s in stats:
            year = int(s['year'])
            week = int(s['week_number'])

            monday = date.fromisocalendar(year, week, 1).strftime("%d.%m.%Y")
            sunday = date.fromisocalendar(year, week, 7).strftime("%d.%m.%Y")
            typer.echo(f"Year {year}, {monday} - {sunday}: {s['num_entries']} entries")
            typer.echo(f"Average mood: {get_printable_rating(round(s['avg_mood']))}")
            typer.echo(f"Average weather rating: {round(s['avg_weather_rating'],1)}/5, {round(s['avg_temperature'],1)}°C")
            typer.echo('------------------------------------------------')
    except ServiceUnavailableException, KeyError, IndexError:
        typer.echo("There has been an error retrieving the statistics.")