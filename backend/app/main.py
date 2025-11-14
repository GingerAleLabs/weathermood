import typer
from model.db import init_db

# db initialization
init_db()

"""
CLI COMMANDS
"""
app = typer.Typer(help="Mood & Weather Tracker CLI")


# --- Command 1: greet ---
@app.command()
def greet(name: str, age: int = 30):
    """Greet someone and show their age."""
    typer.echo(f"Hello {name}, you are {age} years old!")

# --- Command 2: another demo ---
@app.command()
def farewell(name: str):
    """Say goodbye to someone."""
    typer.echo(f"Goodbye {name}!")

#Start the cli
if __name__ == "__main__":
    app()
