import json
from agents import function_tool


@function_tool
def search_hotels(city: str, max_price_per_night: int) -> str:
    """
    Search hotels in a city under the user's maximum nightly budget.
    """
    print("Hotel Tool Called")

    with open("data/mock_hotels.json", "r") as file:
        hotels = json.load(file)

    matching_hotels = []

    for hotel in hotels:
        if (
            hotel["city"].lower() == city.lower()
            and hotel["price_per_night"] <= max_price_per_night
        ):
            matching_hotels.append(hotel)

    if not matching_hotels:
        return "No matching hotels found."

    return json.dumps(matching_hotels, indent=2)