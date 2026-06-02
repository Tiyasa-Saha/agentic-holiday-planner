from agents import Agent
from tools.booking_tools import simulate_booking


booking_agent = Agent(
    name="Booking Agent",
    instructions="""
    You are a booking assistant.
    You can only simulate bookings after the user has clearly approved.
    Never claim that a real payment or real reservation has been made.
    """,
    tools=[simulate_booking],
)