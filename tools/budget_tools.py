from agents import function_tool


@function_tool
def calculate_trip_budget(
    flight_price: int,
    hotel_price_per_night: int,
    number_of_nights: int,
    user_budget: int
) -> str:
    """
    Calculate total estimated trip cost and compare it with the user's budget.
    """

    total_hotel_cost = hotel_price_per_night * number_of_nights
    total_trip_cost = flight_price + total_hotel_cost

    if total_trip_cost <= user_budget:
        status = "within budget"
    else:
        status = "over budget"

    return (
        f"Flight cost: ${flight_price}\n"
        f"Hotel cost: ${hotel_price_per_night} x {number_of_nights} nights = ${total_hotel_cost}\n"
        f"Total estimated trip cost: ${total_trip_cost}\n"
        f"User budget: ${user_budget}\n"
        f"Status: The trip is {status}."
    )