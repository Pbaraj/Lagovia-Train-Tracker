# AI Usage Report

This project was built with support from ChatGPT. AI was used as a development assistant for planning, explanation, debugging, documentation, and review. The final code was run locally, tested, adjusted, and understood before submission.

---

## AI Tool Used

### ChatGPT

I used ChatGPT for:

- Understanding the technical challenge requirements
- Planning the fullstack project structure
- Deciding between backend-only and fullstack implementation
- Designing the backend API response shape
- Building the FastAPI backend step by step
- Connecting the backend to the iRail API
- Debugging iRail API redirect issues
- Debugging Python indentation issues
- Debugging frontend/backend connection and CORS issues
- Creating the React frontend layout
- Improving the frontend UI styling
- Writing backend utility functions
- Writing backend tests
- Preparing the README
- Preparing this AI usage report

---

## Public Chat Links

No public chat link is included because the development conversation was not exported as a public share link.

Instead, this file includes a representative selection of prompts, decisions, accepted suggestions, rewritten parts, and rejected ideas.

---

## Development Plan Created With AI Support

The implementation was planned in the following order:

1. Create a clean fullstack folder structure.
2. Build the backend first using FastAPI.
3. Add the required `/departures?q=...` endpoint.
4. Add validation for queries shorter than 3 characters.
5. Connect to the iRail stations endpoint.
6. Filter station names using case-insensitive substring search.
7. Connect to the iRail liveboard endpoint.
8. Fetch upcoming departures for every matched station.
9. Filter departures scheduled within the next 15 minutes.
10. Convert delay values from seconds to minutes.
11. Return a clean JSON response shape.
12. Build a React frontend using Vite.
13. Add search input, loading state, error state, and empty state.
14. Display departures grouped by station.
15. Improve the frontend styling to look modern and readable.
16. Add backend tests.
17. Run the frontend production build.
18. Write README documentation.
19. Write AI usage documentation.
20. Prepare the project for GitHub submission.

---

## Representative Prompts and Requests Used

The following are examples of the types of prompts and requests used during development:

```text
Explain the technical challenge and recommend whether I should choose backend-only or fullstack.
```

```text
Think like a fullstack software engineer and help me complete this project properly.
```

```text
Help me create the folder structure for a FastAPI backend and React frontend.
```

```text
Create the first FastAPI endpoint for GET /departures?q=Bru with validation for queries shorter than 3 characters.
```

```text
Help me connect to the iRail stations API and filter station names by substring.
```

```text
The iRail API returns a 303 redirect. Help me fix the backend client.
```

```text
Help me fetch live departures from iRail and filter only departures within the next 15 minutes.
```

```text
Create a React frontend that calls the backend and displays departures grouped by station.
```

```text
The frontend shows Failed to fetch. Help me debug the backend/frontend connection.
```

```text
Why is there empty space between station cards in the frontend?
```

```text
Make the frontend look more professional and modern.
```

```text
Write backend tests for validation, station filtering, delay conversion, and time-window filtering.
```

```text
Write a complete README.md for this fullstack technical challenge.
```

```text
Write a complete AI_USAGE.md file for the submission.
```

---

## What I Accepted From AI Suggestions

I accepted AI suggestions for:

- Using FastAPI for the backend
- Using React with Vite for the frontend
- Separating the project into `backend/` and `frontend/`
- Creating a dedicated `irail_client.py` file for external API calls
- Creating a `services.py` file for business logic
- Creating a `utils.py` file for helper functions
- Using a custom JSON response shape instead of returning raw iRail data
- Returning an explicit `QUERY_TOO_SHORT` error for short queries
- Converting iRail delay values from seconds to minutes
- Filtering departures by scheduled departure time
- Adding a frontend debounce before calling the backend
- Showing loading, error, and empty states in the frontend
- Displaying departures grouped by station
- Hiding zero-departure stations in the frontend for readability
- Adding basic backend tests with `pytest`
- Adding a clear README and AI usage report

---

## What I Rewrote, Adjusted, or Verified

I did not blindly copy everything. I adjusted and verified several parts during development.

I rewrote or adjusted:

- The iRail base URL after discovering that the older endpoint redirected to `/v1`
- The CORS configuration to support both `localhost:5173` and `127.0.0.1:5173`
- The error handling so internal debug details are not exposed in the final version
- The frontend display logic so stations with zero upcoming departures are hidden in the UI
- The frontend styling to make it cleaner and more professional
- The README wording
- The AI usage documentation
- Test cases based on the actual implemented functions
- The `.gitignore` file to avoid committing generated and dependency folders

I manually verified:

- The backend starts correctly with Uvicorn
- `/departures?q=Br` returns a 400 validation error
- `/departures?q=Bru` returns real station and departure data
- Departures are filtered to the next 15 minutes
- Delay values are shown in minutes
- The React frontend successfully calls the backend
- Search results are grouped by station
- The frontend displays only stations with actual upcoming departures
- The frontend production build works
- Backend tests pass locally

Final backend test result:

```text
7 passed, 1 warning
```

Final frontend build result:

```text
vite build successful
```

---

## What I Rejected or Postponed

I rejected or postponed the following suggestions or possible features:

- Fuzzy search, because it was listed as a bonus and not required for the base implementation
- A database, because the app only needs live train data and does not need persistence
- Authentication, because it was not part of the challenge
- Calling iRail directly from the frontend, because the backend should control the external API integration
- Complex UI component libraries, because the frontend should stay simple and maintainable
- Deployment setup, because local installation and running were the main submission requirements
- Docker setup, because it was not necessary for the core challenge and could add complexity
- Large-scale caching, because it was not required for the challenge scope

---

## Debugging With AI Support

AI was used to help debug several issues.

### iRail Redirect Issue

The first iRail stations request returned a redirect response:

```text
303 See Other
```

The request was redirected from:

```text
https://api.irail.be/stations/
```

to:

```text
https://api.irail.be/v1/stations
```

The backend client was updated to use:

```text
https://api.irail.be/v1
```

and `follow_redirects=True` was added to the httpx client.

---

### CORS / Frontend Fetch Issue

The frontend initially showed:

```text
Failed to fetch
```

This was solved by checking that the backend was running and by allowing both frontend origins in the backend CORS configuration:

```text
http://localhost:5173
http://127.0.0.1:5173
```

---

### Python Indentation Issue

During development, an indentation error occurred in `main.py`.

The file was cleaned up and indentation was converted to spaces. After this, the backend and tests worked correctly.

---

### Frontend Empty Space Issue

The frontend initially showed cards for stations with zero departures. This created empty visual space between useful station cards.

The UI was adjusted so that the frontend displays only stations that have at least one departure within the next 15 minutes.

The backend still returns all matched stations, keeping the API response complete.

---

## Final Implementation Summary

The final project contains:

### Backend

- FastAPI application
- `/departures` endpoint
- Query validation
- iRail stations integration
- iRail liveboard integration
- Station substring filtering
- 15-minute departure filtering
- Delay conversion from seconds to minutes
- Clean JSON response shape
- CORS configuration for local frontend development
- Basic automated tests

### Frontend

- React + Vite application
- Search input
- Debounced API request
- Loading state
- Error state
- Empty state
- Results grouped by station
- Modern responsive styling
- Departure table showing:
  - Train number
  - Destination
  - Scheduled time
  - Delay

### Documentation

- Complete `README.md`
- Complete `AI_USAGE.md`
- Setup and run instructions
- API contract
- Design decisions
- Trade-offs
- Known limitations
- Test instructions
- Frontend build instructions

---

## Responsibility and Review

AI was used as an assistant, but I remained responsible for the final implementation.

Before submission, I:

- Ran the backend locally
- Ran the frontend locally
- Tested the API manually in the browser
- Checked the frontend output with real iRail data
- Ran the backend test suite
- Ran the frontend production build
- Reviewed and adjusted the documentation

The final project was not submitted as unreviewed AI-generated code. It was tested, debugged, adjusted, and understood locally before submission.

---

## Final Verification

The final local verification results were:

```text
Backend tests: 7 passed, 1 warning
Frontend build: successful
Manual backend test: successful
Manual frontend test: successful
```

The application successfully searched for station substrings such as:

```text
Bru
```

and displayed real upcoming train departures from the public iRail API.