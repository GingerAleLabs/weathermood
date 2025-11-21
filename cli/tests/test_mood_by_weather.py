import pytest
import typer

from typer.testing import CliRunner
from cli.__main__ import app
from backend.services.MoodEntryService import MoodEntryService


def test_mood_by_weather(tmp_path, monkeypatch):
    runner = CliRunner()

    monkeypatch.setenv("WM_DB_PATH", str(tmp_path / "test.db"))

    MoodEntryService.add_entry(
        user_id=None,
        mood = 5,
        note = "Feelin good",
        temperature = 26.4,
        weather_rating = 3
    )

    result = runner.invoke(app, ["mood-by-weather"])

    assert result.exit_code == 0
    assert "Cloudy: ***** (1 entry)" in result.stdout
