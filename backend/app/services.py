import asyncio

from app.irail_client import fetch_stations, fetch_liveboard
from app.utils import filter_stations_by_query, format_departure


async def get_departures_for_query(query: str) -> list[dict]:
    """
    Main business logic:
    1. Fetch all stations.
    2. Filter stations by search query.
    3. Fetch live departures for every matched station.
    4. Keep only departures in the next 15 minutes.
    """
    all_stations = await fetch_stations()
    matched_stations = filter_stations_by_query(all_stations, query)

    results = []

    for station in matched_stations:
        raw_departures = await fetch_liveboard(station["id"])

        filtered_departures = []

        for departure in raw_departures:
            formatted = format_departure(departure)

            if formatted is not None:
                filtered_departures.append(formatted)

        results.append({
            "id": station["id"],
            "name": station["name"],
            "standardName": station["standardName"],
            "departures": filtered_departures,
        })

        # iRail allows 3 requests per second.
        # This small pause keeps us polite and avoids rate-limit problems.
        await asyncio.sleep(0.35)

    return results