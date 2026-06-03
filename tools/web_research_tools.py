from openai import OpenAI
from dotenv import load_dotenv


def research_destination(destination: str, travel_style: str, activity_preference: str) -> str:
    """
    Uses OpenAI web search to find current destination ideas and travel tips.
    """

    load_dotenv()
    client = OpenAI()

    prompt = f"""
    Research current travel ideas for {destination}.

    Traveler preferences:
    - Travel style: {travel_style}
    - Activity preference: {activity_preference}

    Return:
    1. Best neighborhoods
    2. Top attractions
    3. Food recommendations
    4. Safety tips
    5. Why these match the traveler

    Keep it concise.
    """

    response = client.responses.create(
        model="gpt-4.1",
        tools=[
            {"type": "web_search_preview"}
        ],
        input=prompt
    )

    return response.output_text