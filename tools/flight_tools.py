import json
from agents import function_tool
from services.serpapi_service import search_google_flights


CITY_TO_AIRPORT = {
    "boston": "BOS",
    "miami": "MIA",
    "new york": "JFK",
    "los angeles": "LAX",
    "san francisco": "SFO",
    "chicago": "ORD",
    "las vegas": "LAS",
    "seattle": "SEA",
    "orlando": "MCO"
}


def normalize_airport_code(city_or_airport: str) -> str:
    value = city_or_airport.strip().lower()

    if len(value) == 3 and value.isalpha():
        return value.upper()

    return CITY_TO_AIRPORT.get(value, city_or_airport.upper())


@function_tool
def search_flights(
    from_city: str,
    to_city: str,
    outbound_date: str = "2026-07-10",
    return_date: str = "2026-07-13"
) -> str:
    """
    Search real flight options using SerpAPI Google Flights.
    Use airport codes or supported city names.
    """

    departure_id = normalize_airport_code(from_city)
    arrival_id = normalize_airport_code(to_city)

    results = search_google_flights(
        departure_id=departure_id,
        arrival_id=arrival_id,
        outbound_date=outbound_date,
        return_date=return_date
    )

    simplified_flights = []

    all_flights = []

    if "best_flights" in results:
        all_flights.extend(results["best_flights"])

    if "other_flights" in results:
        all_flights.extend(results["other_flights"])

    for index, flight_option in enumerate(all_flights[:5], start=1):
        flights = flight_option.get("flights", [])

        if not flights:
            continue

        first_leg = flights[0]
        last_leg = flights[-1]

        simplified_flights.append({
            "flight_id": f"REAL_FLIGHT_{index}",
            "airline": first_leg.get("airline"),
            "flight_number": first_leg.get("flight_number"),
            "departure_airport": first_leg.get("departure_airport", {}).get("name"),
            "arrival_airport": last_leg.get("arrival_airport", {}).get("name"),
            "departure_time": first_leg.get("departure_airport", {}).get("time"),
            "arrival_time": last_leg.get("arrival_airport", {}).get("time"),
            "duration_minutes": flight_option.get("total_duration"),
            "stops": max(len(flights) - 1, 0),
            "price": flight_option.get("price"),
            "type": "round_trip_real_serpapi"
        })

    if not simplified_flights:
        return "No real flight options found."

    return json.dumps(simplified_flights, indent=2)