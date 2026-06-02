from agents import Agent
from tools.flight_tools import search_flights


flight_agent = Agent(
    name="Flight Agent",
    instructions="""
    You are a flight search specialist.
    Your job is to search available flights and recommend the best options.
    Consider price, number of stops, and travel convenience.
    """,
    tools=[search_flights],
)