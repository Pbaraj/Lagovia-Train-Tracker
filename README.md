# Lagovia Train Tracker

Lagovia Train Tracker is a fullstack web application built for the Digital Product School Engineering Track technical challenge.

The application allows users to search Belgian train stations by typing part of a station name. It returns upcoming departures from every matching station using the public iRail API.

For each departure, the application shows:

- Train number
- Destination
- Scheduled departure time
- Current delay in minutes

Only departures scheduled within the next 15 minutes are returned.

---

## Project Type

This project follows **Track B: Frontend / Fullstack**.

It also includes a reusable backend API endpoint:

```text
GET /departures?q=Bru
```

Therefore, the backend also satisfies the core requirement of **Track A**.

---

## Tech Stack

### Backend

- Python 3.11
- FastAPI
- Uvicorn
- httpx
- pytest

### Frontend

- React
- Vite
- JavaScript
- CSS

### External API

- iRail API
- Stations endpoint
- Liveboard departures endpoint

---

## Main Features

- Search stations by substring
- Case-insensitive station matching
- Minimum query length validation
- Explicit error response for queries shorter than 3 characters
- Real-time station data from iRail
- Real-time liveboard departure data from iRail
- Departures filtered to the next 15 minutes
- Delay converted from seconds to minutes
- Backend returns results grouped by station
- Frontend displays stations with upcoming departures
- Loading, error, and empty states in the frontend
- Backend tests for validation and utility logic

---

## Project Structure

```text
lagovia-train-tracker/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── irail_client.py
│   │   ├── services.py
│   │   └── utils.py
│   │
│   ├── tests/
│   │   ├── test_validation.py
│   │   └── test_utils.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── api.js
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── package-lock.json
│
├── README.md
├── AI_USAGE.md
└── .gitignore
```

---

## API Endpoint

### `GET /departures?q=Bru`

Returns upcoming departures for all stations whose name contains the given query.

The query must contain at least 3 characters.

---

## API Response Shape

### Success Response

```json
{
  "query": "Bru",
  "generatedAt": "2026-05-29T19:13:51.450951+02:00",
  "windowMinutes": 15,
  "matchedStationCount": 16,
  "stations": [
    {
      "id": "BE.NMBS.008813003",
      "name": "Brussels-Central",
      "standardName": "Brussel-Centraal/Bruxelles-Central",
      "departures": [
        {
          "trainNumber": "IC 505",
          "destination": "Eupen",
          "scheduledDepartureTime": "2026-05-29T07:01:00+02:00",
          "delayMinutes": 22
        }
      ]
    }
  ]
}
```

---

### Error Response for Short Query

Request:

```http
GET /departures?q=Br
```

Response:

```json
{
  "detail": {
    "code": "QUERY_TOO_SHORT",
    "message": "Please enter at least 3 characters.",
    "minLength": 3,
    "receivedLength": 2
  }
}
```

HTTP status:

```text
400 Bad Request
```

---

### External API Error Response

If the public iRail API is unavailable or cannot be reached, the backend returns:

```json
{
  "detail": {
    "code": "IRAIL_API_ERROR",
    "message": "Could not fetch departure data from iRail."
  }
}
```

HTTP status:

```text
502 Bad Gateway
```

---

## Prerequisites

Before running the project locally, make sure you have installed:

- Python 3.11
- Conda or another Python environment manager
- Node.js
- npm

Recommended versions:

```text
Python: 3.11
Node.js: 18 or newer
npm: 9 or newer
```

---

## Installation and Running Locally

The backend and frontend are started separately.

---

## Backend Setup

Open a terminal and go to the backend folder:

```bash
cd backend
```

Create a Conda environment:

```bash
conda create -n lagovia python=3.11
```

Activate the environment:

```bash
conda activate lagovia
```

If the environment already exists, just activate it:

```bash
conda activate lagovia
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Run the backend server:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Example backend test URL:

```text
http://127.0.0.1:8000/departures?q=Bru
```

---

## Frontend Setup

Open a second terminal and go to the frontend folder:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Run the frontend:

```bash
npm run dev
```

The frontend will usually run at:

```text
http://localhost:5173
```

Open the frontend in your browser and search for a station substring such as:

```text
Bru
```

---

## Running Backend and Frontend Together

Use two terminals.

### Terminal 1: Backend

```bash
cd backend
conda activate lagovia
uvicorn app.main:app --reload
```

### Terminal 2: Frontend

```bash
cd frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

## Running Tests

Backend tests can be run from the backend folder:

```bash
cd backend
python -m pytest -q
```

Current local test result:

```text
7 passed, 1 warning
```

The warning comes from FastAPI/Starlette TestClient dependency behaviour and does not affect the project functionality.

The tests cover:

- Short query validation
- Empty query validation
- Text normalization
- Case-insensitive station matching
- Train number extraction
- Delay conversion from seconds to minutes
- Filtering departures outside the 15-minute window

---

## Building the Frontend

To verify that the frontend builds successfully:

```bash
cd frontend
npm run build
```

Current local build result:

```text
vite build successful
18 modules transformed
built successfully
```

The generated `frontend/dist/` folder is ignored by Git because it can be rebuilt from the source files.

---

## How the Application Works

1. The user enters a station search query in the frontend.
2. The frontend waits until the query has at least 3 characters.
3. The frontend calls the backend endpoint:

```text
GET /departures?q=<query>
```

4. The backend validates the query.
5. The backend fetches stations from the iRail stations endpoint.
6. The backend filters stations whose name contains the query.
7. For every matched station, the backend calls the iRail liveboard endpoint.
8. The backend filters departures scheduled within the next 15 minutes.
9. The backend converts the delay from seconds to minutes.
10. The backend returns a clean JSON response.
11. The frontend displays the results grouped by station.

---

## Frontend Display Behaviour

The backend returns all matched stations, including stations with zero departures.

For a cleaner user experience, the frontend displays only stations that have at least one departure within the next 15 minutes.

The summary still shows:

- Total matched stations
- Number of stations with upcoming departures
- Total upcoming departures

This keeps the backend complete while making the user interface easier to read.

---

## Design Decisions

### FastAPI for the backend

FastAPI was chosen because it is lightweight, readable, and provides automatic OpenAPI documentation. This makes the API easy to test and explain.

### React with Vite for the frontend

React with Vite was chosen because it is fast to set up and suitable for a small interactive search interface.

### Backend handles iRail communication

The frontend does not call iRail directly. It only communicates with the backend.

This keeps the frontend simpler and allows the backend to control the response shape.

### Custom response shape

The backend converts raw iRail data into a clean response format. This avoids exposing the frontend directly to the external API structure.

### Scheduled departure filtering

Departures are filtered by scheduled departure time because the challenge asks for departures scheduled within the next 15 minutes.

### Delay conversion

iRail returns delay values in seconds. The backend converts this value into minutes before returning it to the frontend.

### No database

No database is used because the application works with live external data and does not need persistence.

### CORS for local development

The backend allows local frontend origins:

```text
http://localhost:5173
http://127.0.0.1:5173
```

This allows the Vite frontend to communicate with the FastAPI backend during local development.

---

## Trade-offs

### Multiple liveboard requests

For every matched station, the backend makes a liveboard request. This is simple and easy to understand, but response time can increase when many stations match the query.

### No persistent caching

The app fetches fresh data from iRail each time. This keeps the data live but means repeated searches may call the external API again.

### Simple backend error handling

External API failures are returned as a clean `502 Bad Gateway` error. Internal debug details are not exposed in the final API response.

### Frontend hides zero-departure stations

The frontend hides stations with zero upcoming departures to improve readability. The backend still returns all matched stations so the API response remains complete.

### No fuzzy search in the base version

The base version implements substring search only. Fuzzy search was considered as a bonus feature but was not prioritized over the required functionality.

---

## Known Limitations

- The application depends on the public iRail API.
- If iRail is slow or unavailable, the application may return an external API error.
- If many stations match a query, response time can increase because several liveboard requests are needed.
- No persistent cache is implemented.
- No fuzzy search is implemented in the base version.
- No deployment configuration is included.
- The frontend is intentionally focused on the challenge requirements.
- The frontend is optimized for local development and not configured for production deployment.

---

## Possible Future Improvements

- Add fuzzy search for misspelled station names.
- Add short-term caching for station and liveboard responses.
- Add a toggle to show or hide stations with zero departures.
- Add sorting by departure time across all stations.
- Add Docker setup for easier fullstack startup.
- Add frontend component tests.
- Add rate-limit handling if many users access the app at the same time.
- Add deployment configuration for a cloud platform.
- Add loading skeletons for a smoother UI.

---

## Troubleshooting

### Frontend shows “Failed to fetch”

Make sure the backend is running:

```bash
cd backend
conda activate lagovia
uvicorn app.main:app --reload
```

Then check this URL in the browser:

```text
http://127.0.0.1:8000/departures?q=Bru
```

If this works, restart the frontend:

```bash
cd frontend
npm run dev
```

---

### Backend cannot fetch iRail data

The backend depends on the public iRail API. If the API is temporarily unavailable or the internet connection is blocked, the backend may return:

```text
IRAIL_API_ERROR
```

---

### npm install does not work

Check that Node.js and npm are installed:

```bash
node -v
npm -v
```

Then run:

```bash
npm install
```

inside the frontend folder.

---

### Conda environment already exists

If this command says the environment already exists:

```bash
conda create -n lagovia python=3.11
```

Do not delete it. Just activate it:

```bash
conda activate lagovia
```

---

## Time Spent

Approximately 8 to 10 hours were spent on:

- Understanding the challenge
- Creating the backend
- Integrating the iRail API
- Debugging API redirects and CORS
- Creating the frontend
- Improving the frontend UI
- Testing the application manually
- Writing backend tests
- Running frontend production build
- Preparing documentation

---

## AI Usage

AI was used during development for planning, implementation support, debugging, and documentation.

A detailed AI usage report is available in:

```text
AI_USAGE.md
```

Summary:

- AI helped plan the project structure.
- AI helped design the backend API shape.
- AI helped debug iRail redirect and CORS issues.
- AI helped create test cases and documentation.
- Final code was reviewed, adjusted, and tested locally before submission.

---

## Final Local Verification

The project was verified locally with:

```text
Backend tests: 7 passed, 1 warning
Frontend build: successful
Manual API test: successful
Manual frontend test: successful
```

Manual test query:

```text
Bru
```

The frontend successfully displayed real iRail departure data grouped by station.

---

## Submission Notes

This project is intended as a clean fullstack technical challenge submission.

The main focus is correctness, clarity, and maintainability:

- Clear backend API
- Simple and modern frontend
- Explicit validation
- Real external API integration
- Readable project structure
- Automated backend tests
- Documented decisions and limitations
- Transparent AI usage report