import typer

from backend.services.ServiceUnavailableException import ServiceUnavailableException
from backend.services.StatsService import StatsService

from cli.utils import get_printable_rating
from datetime import date, timedelta

def aux_weekly_stats(year, month):
    try:
        stats = StatsService.get_weekly_stats(year, month)

        if len(stats) == 0:
            typer.echo("Can't compute the stats, no entries found")
            return

        typer.echo("Weekly stats:")

        for s in stats:
            s_year = int(s['year'])
            s_week = int(s['week_number'])

            #Calculating it for each week to cover the case "filtering by month only"
            period_start, period_end = get_period_bounds(s_year, month)

            w_start = date.fromisocalendar(s_year, s_week, 1)
            w_end   = date.fromisocalendar(s_year, s_week, 7)

            if w_start < period_start:
                w_start = period_start
            if w_end > period_end:
                w_end = period_end

            w_start = w_start.strftime("%d.%m.%Y")
            w_end = w_end.strftime("%d.%m.%Y")

            typer.echo(f"Year {s_year}, {w_start} - {w_end}: {s['num_entries']} {"entries" if s['num_entries'] != 1 else "entry"}")
            typer.echo(f"Average mood: {get_printable_rating(round(s['avg_mood']))}")
            typer.echo(f"Average weather rating: {round(s['avg_weather_rating'],1)}/5, {round(s['avg_temperature'],1)}°C")
            typer.echo('------------------------------------------------')
    except ServiceUnavailableException, KeyError, IndexError:
        typer.echo("There has been an error retrieving the statistics.")


# helper function, determines the boundaries of the weeks in case of filtering
# eg I filter november 2025 -> instead of showing  Year 2025, 27.10.2025 - 02.11.2025: 3 entries
# I only show Year 2025, 01.11.2025 - 02.11.2025: 3 entries
def get_period_bounds(year, month=None):
    if month is not None:
        # month of a specific year
        period_start = date(year, month, 1)

        # compute last day of the month
        if month == 12:
            period_end = date(year, 12, 31)
        else:
            # compute the last day of a month by getting the first day of the following month
            # and then getting the day before (so I don't have to worry about the number of days in a month)
            period_end = date(year, month + 1, 1) - timedelta(days=1)

    else:
        # whole year
        period_start = date(year, 1, 1)
        period_end   = date(year, 12, 31)

    return period_start, period_end