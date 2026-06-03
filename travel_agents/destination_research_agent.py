from agents import Agent, function_tool
from tools.web_research_tools import research_destination


@function_tool
def research_destination_web(
    destination: str,
    travel_style: str,
    activity_preference: str
) -> str:
    """
    Research current destination information using web search.
    Use this for attractions, neighborhoods, local experiences, and travel tips.
    Do not use this for booking or payment.
    """

    return research_destination(
        destination=destination,
        travel_style=travel_style,
        activity_preference=activity_preference
    )


destination_research_agent = Agent(
    name="Destination Research Agent",
    instructions="""
    You are a destination research specialist.

    Your job is to use web search to find current destination information.
    Focus on:
    - neighborhoods
    - attractions
    - local food
    - safety tips
    - travel experiences
    - itinerary ideas

    Do not search for final flight or hotel prices.
    Do not make bookings.
    Do not ask for payment details.
    """,
    tools=[research_destination_web],
)