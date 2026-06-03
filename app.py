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


def show_memory():
    return session_memory.get_memory_summary()


def show_selected_trip():
    selected_trip = session_memory.get_selected_trip()

    if not selected_trip.get("flight_id") or not selected_trip.get("hotel_id"):
        return "No trip selected yet."

    return (
        f"Selected Flight ID: {selected_trip['flight_id']}\n"
        f"Selected Hotel ID: {selected_trip['hotel_id']}"
    )


with gr.Blocks(title="Agentic Holiday Planner") as demo:
    gr.Markdown(
        """
        # Agentic Holiday Planner

        A multi-agent AI travel planning assistant built using the **PRMA framework**.

        **P - Plan:** Understands the user's trip request.  
        **R - Reason:** Compares flights, hotels, itinerary, and budget.  
        **M - Memory:** Remembers user travel preferences during the session.  
        **A - Act:** Simulates booking after user approval.

        **Note:** This version uses mock flight and hotel data. Booking is simulated only.
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(height=500, value=[])

            user_input = gr.Textbox(
                label="Ask the holiday planner",
                placeholder="Example: Plan a trip from Boston to Miami under $900."
            )

            with gr.Row():
                submit_button = gr.Button("Send")
                clear_button = gr.Button("Clear Chat")

        with gr.Column(scale=1):
            gr.Markdown("## Project Debug Panel")

            memory_output = gr.Textbox(
                label="Session Memory",
                lines=8,
                interactive=False
            )

            selected_trip_output = gr.Textbox(
                label="Selected Trip for Booking",
                lines=4,
                interactive=False
            )

            refresh_button = gr.Button("Refresh Debug Info")

            gr.Markdown(
                """
                ### Try these prompts

                1. `I prefer nonstop flights and relaxed beach vacations.`  
                2. `Plan a trip from Boston to Miami under $900.`  
                3. `Yes, book the recommended option.`
                """
            )

    
    def respond(message, chat_history):
        if chat_history is None:
            chat_history = []

        response = chat_with_agent(message, chat_history)

        chat_history = chat_history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response}
        ]

        return "", chat_history, show_memory(), show_selected_trip()

    submit_button.click(
        respond,
        inputs=[user_input, chatbot],
        outputs=[user_input, chatbot, memory_output, selected_trip_output]
    )

    user_input.submit(
        respond,
        inputs=[user_input, chatbot],
        outputs=[user_input, chatbot, memory_output, selected_trip_output]
    )

    refresh_button.click(
        fn=lambda: (show_memory(), show_selected_trip()),
        inputs=[],
        outputs=[memory_output, selected_trip_output]
    )

    clear_button.click(
        fn=lambda: ("", [], "No saved user preferences yet.", "No trip selected yet."),
        inputs=[],
        outputs=[user_input, chatbot, memory_output, selected_trip_output]
    )


if __name__ == "__main__":
    demo.launch()