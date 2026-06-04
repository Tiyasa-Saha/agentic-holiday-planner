from dotenv import load_dotenv
import gradio as gr
from agents import Runner

from travel_agents.request_parser_agent import request_parser_agent
from travel_agents.travel_manager import travel_manager_agent
from memory.session_memory import SessionMemory
from memory.sqlite_memory import SQLiteMemory
# from tools.recommendation_tools import get_best_mock_trip


load_dotenv()

session_memory = SessionMemory()
sqlite_memory = SQLiteMemory()


def show_sqlite_memory(user_id):
    if not user_id:
        return "No user selected."

    return sqlite_memory.format_preferences_for_agent(user_id)


def save_user_preferences(
    user_id,
    flight_preference,
    travel_style,
    activity_preference,
    hotel_budget,
    total_budget
):
    if not user_id:
        return "Please enter a user ID before saving preferences.", "No user selected."

    sqlite_memory.save_preference(user_id, "flight_preference", flight_preference)
    sqlite_memory.save_preference(user_id, "travel_style", travel_style)
    sqlite_memory.save_preference(user_id, "activity_preference", activity_preference)
    sqlite_memory.save_preference(user_id, "hotel_budget_per_night", str(hotel_budget))
    sqlite_memory.save_preference(user_id, "total_budget", str(total_budget))

    return (
        f"Preferences saved for user: {user_id}",
        sqlite_memory.format_preferences_for_agent(user_id)
    )


def reset_user_preferences(user_id):
    if not user_id:
        return "Please enter a user ID before resetting preferences.", "No user selected."

    sqlite_memory.clear_preferences(user_id)

    return (
        f"Preferences reset for user: {user_id}",
        sqlite_memory.format_preferences_for_agent(user_id)
    )


def chat_with_agent(message, history, user_id):
    session_memory.update_from_message(message)

    session_summary = session_memory.get_memory_summary()
    sqlite_summary = sqlite_memory.format_preferences_for_agent(user_id)

    memory_summary = f"""
Session memory:
{session_summary}

Saved profile preferences:
{sqlite_summary}
"""

    parser_input = f"""
    User message:
    {message}

    Saved user preferences:
    {memory_summary}
    """

    parsed_result = Runner.run_sync(request_parser_agent, parser_input)
    travel_request = parsed_result.final_output

    # best_trip = get_best_mock_trip(
    #     origin=travel_request.origin,
    #     destination=travel_request.destination,
    #     hotel_budget_per_night=travel_request.hotel_budget_per_night,
    #     number_of_nights=travel_request.number_of_nights,
    #     total_budget=travel_request.budget
    # )

    # if best_trip:
    #     session_memory.save_selected_trip(
    #         flight_id=best_trip["flight_id"],
    #         hotel_id=best_trip["hotel_id"]
    #     )

    # selected_trip = session_memory.get_selected_trip()
    # best_trip_details = best_trip if best_trip else "No best trip selected from mock data."

    manager_input = f"""
    The user wants help planning a trip.

    Latest user message:
    {message}

    Use this structured travel request:
    {travel_request.model_dump_json(indent=2)}

    Saved user preferences:
    {memory_summary}

    Real flight search is handled by the Flight Agent using SerpAPI Google Flights.

    Real hotel search is handled by the Hotel Agent using SerpAPI Google Hotels.

    Use the available tools to determine the best flight and hotel options.

    When recommending a flight or hotel:
    - Always include the flight_id and hotel_id.
    - Use the same IDs consistently throughout the response.
    - Do not invent alternative IDs.

    If the user asks to book:
    - Use the flight_id and hotel_id from the recommendation that was presented.
    - Booking remains simulated.

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
        **M - Memory:** Remembers user travel preferences during the session and through saved user profiles.  
        **A - Act:** Simulates booking after user approval.

        **Note:** This version uses SerpAPI for real flight and hotel search. Booking is simulated only.
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(height=500, value=[])

            user_input = gr.Textbox(
                label="Ask the holiday planner",
                placeholder="Example: Plan a trip from Boston to Miami."
            )

            with gr.Row():
                submit_button = gr.Button("Send")
                clear_button = gr.Button("Clear Chat")

        with gr.Column(scale=1):
            gr.Markdown("## Preference Manager")

            user_id_input = gr.Textbox(
                label="User ID",
                value="tiyasa",
                placeholder="Example: tiyasa"
            )

            flight_preference_dropdown = gr.Dropdown(
                label="Flight Preference",
                choices=["no preference", "nonstop", "cheapest", "shortest duration"],
                value="nonstop"
            )

            travel_style_dropdown = gr.Dropdown(
                label="Travel Style",
                choices=["relaxed", "adventure", "luxury", "budget-friendly", "family-friendly"],
                value="relaxed"
            )

            activity_preference_dropdown = gr.Dropdown(
                label="Activity Preference",
                choices=["general sightseeing", "beach", "food", "nightlife", "nature", "culture"],
                value="beach"
            )

            hotel_budget_slider = gr.Slider(
                label="Hotel Budget Per Night",
                minimum=50,
                maximum=500,
                value=150,
                step=10
            )

            total_budget_slider = gr.Slider(
                label="Total Trip Budget",
                minimum=300,
                maximum=5000,
                value=900,
                step=50
            )

            with gr.Row():
                save_preferences_button = gr.Button("Save Preferences")
                reset_preferences_button = gr.Button("Reset Preferences")

            preference_status_output = gr.Textbox(
                label="Preference Status",
                lines=2,
                interactive=False
            )

            sqlite_memory_output = gr.Textbox(
                label="Saved Profile Preferences",
                lines=8,
                interactive=False
            )

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

                1. Save preferences from the Preference Manager.  
                2. `Plan a trip from Boston to Miami.`  
                3. `Yes, book the recommended option.`
                """
            )

    def respond(message, chat_history, user_id):
        if chat_history is None:
            chat_history = []

        response = chat_with_agent(message, chat_history, user_id)

        chat_history = chat_history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response}
        ]

        return (
            "",
            chat_history,
            show_memory(),
            show_selected_trip(),
            show_sqlite_memory(user_id)
        )

    submit_button.click(
        respond,
        inputs=[user_input, chatbot, user_id_input],
        outputs=[
            user_input,
            chatbot,
            memory_output,
            selected_trip_output,
            sqlite_memory_output
        ]
    )

    user_input.submit(
        respond,
        inputs=[user_input, chatbot, user_id_input],
        outputs=[
            user_input,
            chatbot,
            memory_output,
            selected_trip_output,
            sqlite_memory_output
        ]
    )

    save_preferences_button.click(
        save_user_preferences,
        inputs=[
            user_id_input,
            flight_preference_dropdown,
            travel_style_dropdown,
            activity_preference_dropdown,
            hotel_budget_slider,
            total_budget_slider
        ],
        outputs=[
            preference_status_output,
            sqlite_memory_output
        ]
    )

    reset_preferences_button.click(
        reset_user_preferences,
        inputs=[user_id_input],
        outputs=[
            preference_status_output,
            sqlite_memory_output
        ]
    )

    refresh_button.click(
        fn=lambda user_id: (
            show_memory(),
            show_selected_trip(),
            show_sqlite_memory(user_id)
        ),
        inputs=[user_id_input],
        outputs=[
            memory_output,
            selected_trip_output,
            sqlite_memory_output
        ]
    )

    clear_button.click(
        fn=lambda: (
            "",
            [],
            "No saved user preferences yet.",
            "No trip selected yet.",
            "No user selected."
        ),
        inputs=[],
        outputs=[
            user_input,
            chatbot,
            memory_output,
            selected_trip_output,
            sqlite_memory_output
        ]
    )


if __name__ == "__main__":
    demo.launch()