from datetime import datetime
import typer

def print_entry(entry): 
    try:
        dt = datetime.fromisoformat(entry['timestamp'])
        typer.echo(dt.strftime("%A, %d %B %Y %H:%M"))
        typer.echo(f"Mood: {get_printable_rating(entry['mood'])}")
        typer.echo(f"Weather: {entry['weather_description']}, {entry['temperature']}°C")
        if not (entry['note']==""):
            typer.echo(f">> {entry['note']}")
        typer.echo('------------------------------------------------')
    except KeyError, ValueError, IndexError:
        typer.echo("Error printing the entry") #Should never happen


def get_printable_rating(rating):
    try:
        stars=['*----', '**---', '***--', '****-', '*****']
        return stars[rating-1]
    except IndexError:
        typer.echo("-----") #should never happen