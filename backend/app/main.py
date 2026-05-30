from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.services import get_departures_for_query

BRUSSELS_TIMEZONE = ZoneInfo("Europe/Brussels")

app = FastAPI(
    title="Lagovia Train Tracker API",
    description="Backend API for searching Belgian train departures using iRail.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Lagovia Train Tracker API is running",
        "docs": "/docs",
    }


@app.get("/departures")
async def get_departures(q: str = Query(..., description="Station search query")):
    cleaned_query = q.strip()

    if len(cleaned_query) < 3:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "QUERY_TOO_SHORT",
                "message": "Please enter at least 3 characters.",
                "minLength": 3,
                "receivedLength": len(cleaned_query),
            },
        )

    try:
        stations = await get_departures_for_query(cleaned_query)
    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail={
                "code": "IRAIL_API_ERROR",
                "message": "Could not fetch departure data from iRail.",
            },
        )

    return {
        "query": cleaned_query,
        "generatedAt": datetime.now(BRUSSELS_TIMEZONE).isoformat(),
        "windowMinutes": 15,
        "matchedStationCount": len(stations),
        "stations": stations,
    }