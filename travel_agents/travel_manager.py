from agents import Agent

from travel_agents.flight_agent import flight_agent
from travel_agents.hotel_agent import hotel_agent
from travel_agents.budget_agent import budget_agent
from travel_agents.itinerary_agent import itinerary_agent
from travel_agents.booking_agent import booking_agent


travel_manager_agent = Agent(
    name="Travel Manager Agent",
    instructions="""
    You are the main travel planning manager.

    You help users plan holidays using the PRMA framework:

    P - Plan:
    Understand the user's destination, travel dates, budget, number of days,
    departure city, hotel preferences, and travel style.

    R - Reason:
    Compare flight, hotel, itinerary, and budget information before giving a recommendation.

    M - Memory:
    Remember user preferences during the conversation, such as budget, travel style,
    preferred hotel type, and flight preferences.

    A - Act:
    Use the specialist agents as tools when needed.

    Important rules:
    - Ask for missing information if the user's request is incomplete.
    - Recommend options clearly.
    - Do not make a real booking.
    - Only simulate booking after the user clearly approves.
    """,
    tools=[
        flight_agent.as_tool(
            tool_name="search_and_compare_flights",
            tool_description="Search and compare flight options."
        ),
        hotel_agent.as_tool(
            tool_name="search_and_compare_hotels",
            tool_description="Search and compare hotel options."
        ),
        budget_agent.as_tool(
            tool_name="analyze_trip_budget",
            tool_description="Analyze whether the trip is within the user's budget."
        ),
        itinerary_agent.as_tool(
            tool_name="create_trip_itinerary",
            tool_description="Create a day-by-day travel itinerary."
        ),
        booking_agent.as_tool(
            tool_name="simulate_trip_booking",
            tool_description="Simulate a booking only after user approval."
        ),
    ],
)