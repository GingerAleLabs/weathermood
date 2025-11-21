import pytest
import typer

from typer.testing import CliRunner
from cli.__main__ import app
from backend.services.MoodEntryService import MoodEntryService


def test_list_entries(tmp_path, monkeypatch):
    runner = CliRunner()

    monkeypatch.setenv("WM_DB_PATH", str(tmp_path / "test.db"))

    MoodEntryService.add_entry(
        user_id=None,
        mood = 5,
        note = "Feelin good",
        temperature = 26.4,
        weather_rating = 3
    )

    result = runner.invoke(app, ["list-entries"])

    assert result.exit_code == 0
    assert "*****" in result.stdout
    assert "Feelin good" in result.stdout
    assert "26.4" in result.stdout
    assert "Cloudy" in result.stdout

