import httpx

IRAIL_BASE_URL = "https://api.irail.be/v1"

HEADERS = {
    "User-Agent": "LagoviaTrainTracker/0.1 (Digital Product School challenge)"
}


async def fetch_stations():
    """
    Fetch all stations from the public iRail API.
    """
    params = {
        "format": "json",
        "lang": "en",
    }

    async with httpx.AsyncClient(
        timeout=10.0,
        headers=HEADERS,
        follow_redirects=True,
    ) as client:
        response = await client.get(f"{IRAIL_BASE_URL}/stations", params=params)
        response.raise_for_status()
        data = response.json()

    stations = data.get("station", [])

    if isinstance(stations, dict):
        stations = [stations]

    return stations


async def fetch_liveboard(station_id: str):
    """
    Fetch live departures for one station from iRail.
    """
    params = {
        "id": station_id,
        "arrdep": "departure",
        "format": "json",
        "lang": "en",
        "alerts": "false",
    }

    async with httpx.AsyncClient(
        timeout=10.0,
        headers=HEADERS,
        follow_redirects=True,
    ) as client:
        response = await client.get(f"{IRAIL_BASE_URL}/liveboard", params=params)
        response.raise_for_status()
        data = response.json()

    departures_data = data.get("departures", {})
    departures = departures_data.get("departure", [])

    if isinstance(departures, dict):
        departures = [departures]

    return departures