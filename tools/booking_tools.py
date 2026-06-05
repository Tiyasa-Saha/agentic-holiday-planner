from agents import function_tool
import random


@function_tool
def simulate_booking(flight_id: str, hotel_id: str, user_approved: bool) -> str:
    """
    Simulate a travel booking after user approval.
    This does not make a real booking, reservation, or payment.
    """

    if not user_approved:
        return "Booking not completed. User approval is required."

    if not flight_id or not hotel_id:
        return "Booking not completed. Both flight_id and hotel_id are required."

    booking_id = "SIM-" + str(random.randint(10000, 99999))

    return (
        "Simulated booking confirmed successfully.\n"
        f"Simulated Booking ID: {booking_id}\n"
        f"Flight ID: {flight_id}\n"
        f"Hotel ID: {hotel_id}\n\n"
        "Important: This is not a real booking.\n"
        "No real flight ticket was issued.\n"
        "No real hotel reservation was made.\n"
        "No payment was processed."
    )