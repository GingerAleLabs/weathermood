from backend.services.MoodEntryService import MoodEntryService
from backend.services.ServiceUnavailableException import ServiceUnavailableException
from cli.utils import print_entry

import typer



def aux_list_entries(year, month):
    try:
        entries = MoodEntryService.get_entries(year, month)

        if not entries:
            typer.echo("No entries found.")
            return

        for e in entries:
            print_entry(e)
    except ServiceUnavailableException as e:
        typer.echo("There has been an error retrieving the entries.")