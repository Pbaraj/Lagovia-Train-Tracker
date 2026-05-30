const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchDepartures(query) {
  const response = await fetch(
    `${API_BASE_URL}/departures?q=${encodeURIComponent(query)}`
  );

  const data = await response.json();

  if (!response.ok) {
    const message =
      data.detail?.message ||
      data.detail?.error?.message ||
      "Something went wrong while fetching departures.";

    throw new Error(message);
  }

  return data;
}