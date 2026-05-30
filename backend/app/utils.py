from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

BRUSSELS_TIMEZONE = ZoneInfo("Europe/Brussels")


def normalize_text(value: str) -> str:
    """
    Normalize text for case-insensitive substring matching.
    """
    return value.strip().lower()


def filter_stations_by_query(stations: list[dict], query: str) -> list[dict]:
    """
    Return stations whose English name or standard name contains the query.
    Matching is case-insensitive.
    """
    normalized_query = normalize_text(query)
    matched_stations = []

    for station in stations:
        name = station.get("name", "")
        standard_name = station.get("standardname", "")

        searchable_text = f"{name} {standard_name}".lower()

        if normalized_query in searchable_text:
            matched_stations.append({
                "id": station.get("id"),
                "name": name or standard_name,
                "standardName": standard_name,
                "departures": [],
            })

    return matched_stations


def unix_timestamp_to_datetime(timestamp: int) -> datetime:
    """
    Convert iRail Unix timestamp to timezone-aware Brussels datetime.
    """
    return datetime.fromtimestamp(int(timestamp), tz=BRUSSELS_TIMEZONE)


def is_within_next_minutes(departure_time: datetime, minutes: int = 15) -> bool:
    """
    Check if a scheduled departure is between now and now + given minutes.
    """
    now = datetime.now(BRUSSELS_TIMEZONE)
    window_end = now + timedelta(minutes=minutes)

    return now <= departure_time <= window_end


def extract_train_number(departure: dict) -> str:
    """
    Extract train number from iRail departure object.
    Prefer vehicleinfo.shortname, fallback to vehicle.
    """
    vehicle_info = departure.get("vehicleinfo", {})
    short_name = vehicle_info.get("shortname")

    if short_name:
        return short_name

    vehicle = departure.get("vehicle", "")

    if vehicle.startswith("BE.NMBS."):
        return vehicle.replace("BE.NMBS.", "")

    return vehicle


def format_departure(departure: dict) -> dict | None:
    """
    Convert raw iRail departure into our clean API response shape.
    Returns None if departure has invalid/missing time.
    """
    raw_time = departure.get("time")

    if raw_time is None:
        return None

    scheduled_time = unix_timestamp_to_datetime(int(raw_time))

    if not is_within_next_minutes(scheduled_time, minutes=15):
        return None

    delay_seconds = int(departure.get("delay", 0))
    delay_minutes = delay_seconds // 60

    return {
        "trainNumber": extract_train_number(departure),
        "destination": departure.get("station", "Unknown destination"),
        "scheduledDepartureTime": scheduled_time.isoformat(),
        "delayMinutes": delay_minutes,
    }