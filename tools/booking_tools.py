from agents import function_tool
import random


@function_tool
def simulate_booking(flight_id: str, hotel_id: str, user_approved: bool) -> str:
    """
    Simulate a travel booking after user approval.
    This does not make a real booking or payment.
    """

    if not user_approved:
        return "Booking not completed. User approval is required."

    booking_id = "BK" + str(random.randint(10000, 99999))

    return (
        "Booking confirmed successfully.\n"
        f"Booking ID: {booking_id}\n"
        f"Flight ID: {flight_id}\n"
        f"Hotel ID: {hotel_id}\n"
        "Note: This is a simulated booking. No real payment was made."
    )