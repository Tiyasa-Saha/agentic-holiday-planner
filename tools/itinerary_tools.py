from agents import function_tool


@function_tool
def create_itinerary(destination: str, number_of_days: int, travel_style: str) -> str:
    """
    Create a simple day-by-day itinerary for the destination.
    """

    itinerary = []

    for day in range(1, number_of_days + 1):
        itinerary.append(
            f"Day {day}: Explore {destination} with a {travel_style} travel style. "
            f"Include sightseeing, food, and relaxation."
        )

    return "\n".join(itinerary)