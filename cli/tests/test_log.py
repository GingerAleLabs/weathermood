import pytest
import typer

from cli.log import aux_log


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


