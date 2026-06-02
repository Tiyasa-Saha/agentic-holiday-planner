import json
from agents import function_tool


@function_tool
def search_flights(from_city: str, to_city: str) -> str:
    """
    Search available flights from one city to another using mock flight data.
    """

    print("Flight Tool Called")

    with open("data/mock_flights.json", "r") as file:
        flights = json.load(file)

    matching_flights = []

    for flight in flights:
        if (
            flight["from_city"].lower() == from_city.lower()
            and flight["to_city"].lower() == to_city.lower()
        ):
            matching_flights.append(flight)

    if not matching_flights:
        return "No matching flights found."

    return json.dumps(matching_flights, indent=2)