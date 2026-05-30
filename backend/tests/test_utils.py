from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.utils import (
    normalize_text,
    filter_stations_by_query,
    extract_train_number,
    format_departure,
)

BRUSSELS_TIMEZONE = ZoneInfo("Europe/Brussels")


def test_normalize_text_removes_spaces_and_lowercases():
    assert normalize_text("  Bru  ") == "bru"


def test_filter_stations_by_query_matches_case_insensitive_substring():
    stations = [
        {
            "id": "1",
            "name": "Brussels-Central",
            "standardname": "Brussel-Centraal/Bruxelles-Central",
        },
        {
            "id": "2",
            "name": "Antwerp-Central",
            "standardname": "Antwerpen-Centraal",
        },
    ]

    result = filter_stations_by_query(stations, "bru")

    assert len(result) == 1
    assert result[0]["name"] == "Brussels-Central"


def test_extract_train_number_prefers_vehicleinfo_shortname():
    departure = {
        "vehicle": "BE.NMBS.IC1234",
        "vehicleinfo": {
            "shortname": "IC 1234"
        },
    }

    assert extract_train_number(departure) == "IC 1234"


def test_format_departure_converts_delay_seconds_to_minutes():
    departure_time = datetime.now(BRUSSELS_TIMEZONE) + timedelta(minutes=5)

    departure = {
        "time": str(int(departure_time.timestamp())),
        "delay": "180",
        "station": "Antwerp-Central",
        "vehicle": "BE.NMBS.IC1234",
        "vehicleinfo": {
            "shortname": "IC 1234"
        },
    }

    result = format_departure(departure)

    assert result is not None
    assert result["trainNumber"] == "IC 1234"
    assert result["destination"] == "Antwerp-Central"
    assert result["delayMinutes"] == 3


def test_format_departure_filters_departures_outside_15_minutes():
    departure_time = datetime.now(BRUSSELS_TIMEZONE) + timedelta(minutes=30)

    departure = {
        "time": str(int(departure_time.timestamp())),
        "delay": "0",
        "station": "Antwerp-Central",
        "vehicle": "BE.NMBS.IC1234",
        "vehicleinfo": {
            "shortname": "IC 1234"
        },
    }

    result = format_departure(departure)

    assert result is None