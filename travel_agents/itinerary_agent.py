from agents import Agent
from tools.itinerary_tools import create_itinerary


itinerary_agent = Agent(
    name="Itinerary Agent",
    instructions="""
    You are a travel itinerary specialist.
    Your job is to create simple, realistic day-by-day travel plans.
    Keep the itinerary useful, clear, and beginner-friendly.
    """,
    tools=[create_itinerary],
)