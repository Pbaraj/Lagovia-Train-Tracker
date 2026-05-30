import { useEffect, useState } from "react";
import { fetchDepartures } from "./api";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [departuresData, setDeparturesData] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const cleanedQuery = query.trim();

    if (cleanedQuery.length < 3) {
      setDeparturesData(null);
      setError("Please enter at least 3 characters.");
      setIsLoading(false);
      return;
    }

    const timeoutId = setTimeout(async () => {
      try {
        setIsLoading(true);
        setError("");

        const data = await fetchDepartures(cleanedQuery);
        setDeparturesData(data);
      } catch (err) {
        setDeparturesData(null);
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    }, 400);

    return () => clearTimeout(timeoutId);
  }, [query]);

  const allStations = departuresData?.stations || [];

  const stationsWithDepartures = allStations.filter(
    (station) => station.departures.length > 0
  );

  const totalDepartures = allStations.reduce(
    (total, station) => total + station.departures.length,
    0
  );

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">Lagovia Train Tracker</p>

        <h1>Belgian train delays, searched by station.</h1>

        <p className="subtitle">
          Type at least three characters to find stations and see departures
          scheduled within the next 15 minutes.
        </p>

        <input
          className="search-input"
          type="text"
          placeholder="Try Bru, Aac, Gent..."
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </section>

      {isLoading && <p className="status">Loading departures...</p>}

      {!isLoading && error && <p className="error">{error}</p>}

      {!isLoading && departuresData && (
        <section className="results-summary">
          <p>
            Found <strong>{departuresData.matchedStationCount}</strong> matching
            stations. Showing <strong>{stationsWithDepartures.length}</strong>{" "}
            stations with upcoming departures and{" "}
            <strong>{totalDepartures}</strong> total departures.
          </p>
        </section>
      )}

      {!isLoading && departuresData && totalDepartures === 0 && (
        <p className="status">
          No departures scheduled in the next 15 minutes for this search.
        </p>
      )}

      <section className="stations">
        {stationsWithDepartures.map((station) => (
          <article className="station-card" key={station.id}>
            <div className="station-header">
              <h2>{station.name}</h2>
              <span>{station.departures.length} departures</span>
            </div>

            <table>
              <thead>
                <tr>
                  <th>Train</th>
                  <th>Destination</th>
                  <th>Scheduled time</th>
                  <th>Delay</th>
                </tr>
              </thead>

              <tbody>
                {station.departures.map((departure, index) => (
                  <tr key={`${station.id}-${departure.trainNumber}-${index}`}>
                    <td>{departure.trainNumber}</td>
                    <td>{departure.destination}</td>
                    <td>
                      {new Date(
                        departure.scheduledDepartureTime
                      ).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </td>
                    <td>
                      {departure.delayMinutes === 0
                        ? "On time"
                        : `+${departure.delayMinutes} min`}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </article>
        ))}
      </section>
    </main>
  );
}

export default App;