import pytest
import typer

from typer.testing import CliRunner
from cli.__main__ import app
from backend.services.MoodEntryService import MoodEntryService


def test_weekly_stats(tmp_path, monkeypatch):
    runner = CliRunner()

    monkeypatch.setenv("WM_DB_PATH", str(tmp_path / "test.db"))

    MoodEntryService.add_entry(
        user_id=None,
        mood = 5,
        note = "Feelin good",
        temperature = 26.4,
        weather_rating = 3
    )

    result = runner.invoke(app, ["weekly-stats"])

    assert result.exit_code == 0
    assert "*****" in result.stdout
    assert "3" in result.stdout
    assert "1 entry" in result.stdout