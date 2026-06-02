from agents import Agent
from models.travel_request import TravelRequest


request_parser_agent = Agent(
    name="Travel Request Parser Agent",
    instructions="""
    You extract structured travel request details from the user message and saved memory.

    Use these default values when details are missing:
    - number_of_days: 3
    - number_of_nights: 3
    - number_of_travelers: 1
    - hotel_budget_per_night: 150
    - travel_style: relaxed
    - flight_preference: no specific flight preference
    - activity_preference: general sightseeing

    Rules:
    - Extract origin and destination from the user message.
    - Extract budget as a number only. Example: "$900" becomes 900.
    - Use saved memory if the user message does not repeat a preference.
    - Do not invent origin or destination if missing.
    - If origin or destination is missing, set it to "unknown".
    """,
    output_type=TravelRequest,
)