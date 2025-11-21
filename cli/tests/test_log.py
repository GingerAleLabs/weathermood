import pytest
import typer
from typer.testing import CliRunner

from cli.log import aux_log
from cli.__main__ import app
from backend.services.MoodEntryService import MoodEntryService

def test_log(tmp_path, monkeypatch):
	runner = CliRunner()

	monkeypatch.setenv("WM_DB_PATH", str(tmp_path / "test.db"))

	result1 = runner.invoke(app, ["log", "-mood", "5", "-note", "Good day", "-city", "Sydney"])
	result2 = runner.invoke(app, ["log", "-mood", "5", "-note", "Good day", "-lat", "-45", "-lng", "80"])

	assert result1.exit_code == 0
	assert "Logged" in result1.stdout

	assert result2.exit_code == 0
	assert "Logged" in result2.stdout

	entries = MoodEntryService.get_entries()

	assert len(entries) == 2



def test_reject_city_and_coords_together():
	with pytest.raises(typer.BadParameter):
		aux_log(mood=3, note="n", city="Rome", lat=41.9, lng=12.5)


def test_unsupported_city():
    with pytest.raises(typer.BadParameter):
        aux_log(mood=3, note="n", city="Unknown City", lat=None, lng=None)


def test_missing_both_city_and_coords():
	with pytest.raises(typer.BadParameter):
		aux_log(mood=4, note="n", city=None, lat=None, lng=None)


def test_missing_one_coord():
	with pytest.raises(typer.BadParameter):
		aux_log(mood=4, note="n", city=None, lat=10.0, lng=None)


def test_lat_bounds():
	with pytest.raises(typer.BadParameter):
		aux_log(mood=4, note="n", city=None, lat=100.0, lng=0.0)


def test_lng_bounds():
	with pytest.raises(typer.BadParameter):
		aux_log(mood=4, note="n", city=None, lat=0.0, lng=200.0)


