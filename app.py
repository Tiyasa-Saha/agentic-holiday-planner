from dotenv import load_dotenv
import gradio as gr
from agents import Runner

from travel_agents.request_parser_agent import request_parser_agent
from travel_agents.travel_manager import travel_manager_agent
from memory.session_memory import SessionMemory
from tools.recommendation_tools import get_best_mock_trip


load_dotenv()

session_memory = SessionMemory()


def chat_with_agent(message, history):
    session_memory.update_from_message(message)
    memory_summary = session_memory.get_memory_summary()

    parser_input = f"""
    User message:
    {message}

    Saved user preferences from this session:
    {memory_summary}
    """

    parsed_result = Runner.run_sync(request_parser_agent, parser_input)
    travel_request = parsed_result.final_output

    best_trip = get_best_mock_trip(
        origin=travel_request.origin,
        destination=travel_request.destination,
        hotel_budget_per_night=travel_request.hotel_budget_per_night,
        number_of_nights=travel_request.number_of_nights,
        total_budget=travel_request.budget
    )

    if best_trip:
        session_memory.save_selected_trip(
            flight_id=best_trip["flight_id"],
            hotel_id=best_trip["hotel_id"]
        )

    selected_trip = session_memory.get_selected_trip()
    best_trip_details = best_trip if best_trip else "No best trip selected from mock data."

    manager_input = f"""
    The user wants help planning a trip.

    Latest user message:
    {message}

    Use this structured travel request:
    {travel_request.model_dump_json(indent=2)}

    Saved user preferences:
    {memory_summary}

    Selected trip for booking, if available:
    {selected_trip}

    Best mock trip selected by app-side recommendation logic:
    {best_trip_details}

    If the user asks to book the recommended option and selected_trip has a flight_id and hotel_id,
    use those IDs for the simulated booking.

    Now create the best travel plan using the available specialist agents and tools.
    """

    final_result = Runner.run_sync(travel_manager_agent, manager_input)
    return final_result.final_output


demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="Agentic Holiday Planner",
    description="Plan trips using a multi-agent PRMA holiday planner.",
)


if __name__ == "__main__":
    demo.launch()