from agents import Agent
from tools.hotel_tools import search_hotels


hotel_agent = Agent(
    name="Hotel Agent",
    instructions="""
    You are a hotel search specialist.
    Your job is to find hotels based on destination, budget, rating, and amenities.
    Recommend practical options clearly.
    """,
    tools=[search_hotels],
)