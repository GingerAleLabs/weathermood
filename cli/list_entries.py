from backend.app.services.MoodEntryService import MoodEntryService

from datetime import datetime
import typer

def print_entry(entry):
    stars=['*----', '**---', '***--', '****-', '*****']
    dt = datetime.fromisoformat(entry['timestamp'])
    typer.echo(dt.strftime("%A, %d %B %Y %H:%M"))
    typer.echo(f"Mood: {stars[entry['mood']-1]}")
    typer.echo(f"Weather: {entry['weather_description']}, {entry['temperature']}°C")
    if not (entry['note']==""):
        typer.echo(f">> {entry['note']}")
    typer.echo('------------------------------------------------')

def aux_list_entries():
    entries = MoodEntryService.get_entries()

    if not entries:
        typer.echo("No entries found.")
        return

    for e in entries:
        print_entry(e)