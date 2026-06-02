from agents import Agent
from tools.budget_tools import calculate_trip_budget


budget_agent = Agent(
    name="Budget Agent",
    instructions="""
    You are a budget analysis specialist.
    Your job is to calculate the estimated trip cost and check if it fits the user's budget.
    Explain costs clearly and simply.
    """,
    tools=[calculate_trip_budget],
)