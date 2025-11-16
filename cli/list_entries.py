from backend.app.services.MoodEntryService import MoodEntryService
from cli.utils import print_entry

import typer



def aux_list_entries():
    entries = MoodEntryService.get_entries()

    if not entries:
        typer.echo("No entries found.")
        return

    for e in entries:
        print_entry(e)