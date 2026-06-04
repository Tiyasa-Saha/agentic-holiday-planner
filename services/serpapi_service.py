import os
import requests
from dotenv import load_dotenv


load_dotenv()


def test_serpapi_connection() -> dict:
    """
    Test whether the SerpAPI key is valid by making a simple Google search request.
    """

    api_key = os.getenv("SERPAPI_API_KEY")
    base_url = os.getenv("SERPAPI_BASE_URL", "https://serpapi.com/search")

    if not api_key:
        raise ValueError("Missing SERPAPI_API_KEY in .env")

    params = {
        "engine": "google",
        "q": "Miami travel guide",
        "api_key": api_key
    }

    response = requests.get(base_url, params=params, timeout=30)

    if response.status_code != 200:
        raise Exception(
            f"SerpAPI connection failed. "
            f"Status code: {response.status_code}. "
            f"Response: {response.text}"
        )

    return response.json()

def search_google_flights(
    departure_id: str,
    arrival_id: str,
    outbound_date: str,
    return_date: str,
    currency: str = "USD"
) -> dict:
    """
    Search real flight options using SerpAPI Google Flights.
    Dates must be in YYYY-MM-DD format.
    Airport codes should be used, for example BOS and MIA.
    """

    api_key = os.getenv("SERPAPI_API_KEY")
    base_url = os.getenv("SERPAPI_BASE_URL", "https://serpapi.com/search")

    if not api_key:
        raise ValueError("Missing SERPAPI_API_KEY in .env")

    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": currency,
        "api_key": api_key
    }

    response = requests.get(base_url, params=params, timeout=30)

    if response.status_code != 200:
        raise Exception(
            f"Google Flights search failed. "
            f"Status code: {response.status_code}. "
            f"Response: {response.text}"
        )

    return response.json()