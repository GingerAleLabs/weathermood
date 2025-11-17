from datetime import datetime
import typer

def print_entry(entry): 
    dt = datetime.fromisoformat(entry['timestamp'])
    typer.echo(dt.strftime("%A, %d %B %Y %H:%M"))
    typer.echo(f"Mood: {get_printable_rating(entry['mood'])}")
    typer.echo(f"Weather: {entry['weather_description']}, {entry['temperature']}°C")
    if not (entry['note']==""):
        typer.echo(f">> {entry['note']}")
    typer.echo('------------------------------------------------')


def get_printable_rating(rating):
    stars=['*----', '**---', '***--', '****-', '*****']
    return stars[rating-1]