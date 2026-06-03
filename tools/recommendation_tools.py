import json


def get_best_mock_trip(
    origin: str,
    destination: str,
    hotel_budget_per_night: int,
    number_of_nights: int,
    total_budget: int
) -> dict:
    """
    Finds the best mock flight and hotel combination.
    This is app-side logic, not an agent tool yet.
    """

    with open("data/mock_flights.json", "r") as file:
        flights = json.load(file)

    with open("data/mock_hotels.json", "r") as file:
        hotels = json.load(file)

    matching_flights = [
        flight for flight in flights
        if flight["from_city"].lower() == origin.lower()
        and flight["to_city"].lower() == destination.lower()
    ]

    matching_hotels = [
        hotel for hotel in hotels
        if hotel["city"].lower() == destination.lower()
        and hotel["price_per_night"] <= hotel_budget_per_night
    ]

    if not matching_flights or not matching_hotels:
        return {}

    best_trip = None
    best_score = float("inf")

    for flight in matching_flights:
        round_trip_flight_cost = flight["price"] * 2

        for hotel in matching_hotels:
            hotel_total = hotel["price_per_night"] * number_of_nights
            total_cost = round_trip_flight_cost + hotel_total

            if total_cost <= total_budget:
                score = total_cost

                if flight["stops"] == 0:
                    score -= 50

                if hotel["rating"] >= 4.5:
                    score -= 30

                if score < best_score:
                    best_score = score
                    best_trip = {
                        "flight_id": flight["flight_id"],
                        "hotel_id": hotel["hotel_id"],
                        "flight": flight,
                        "hotel": hotel,
                        "round_trip_flight_cost": round_trip_flight_cost,
                        "hotel_total": hotel_total,
                        "total_cost": total_cost
                    }

    return best_trip or {}