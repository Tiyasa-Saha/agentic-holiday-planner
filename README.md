# Agentic Holiday Planner

An AI-powered holiday planning assistant built using a multi-agent architecture and the PRMA framework.

The assistant can understand a user's travel request, remember preferences, compare mock flight and hotel options, generate a simple itinerary, check budget fit, and simulate a booking after user approval.

## PRMA Framework

This project is designed around the PRMA framework:

* **P - Plan:** Understands the user's destination, budget, trip length, and travel preferences.
* **R - Reason:** Compares flight, hotel, itinerary, and budget information before recommending an option.
* **M - Memory:** Remembers user preferences during the session, such as nonstop flights or beach vacations.
* **A - Act:** Uses tools and agents to search options, recommend a trip, and simulate booking.

## Features

* Multi-agent travel planning system
* Request parser agent for structured travel inputs
* Flight search agent using mock flight data
* Hotel search agent using mock hotel data
* Budget analysis
* Itinerary generation
* Session memory for user preferences
* Dynamic recommended trip selection
* Simulated booking flow
* Gradio web interface with debug panel

## Tech Stack

* Python
* OpenAI Agents SDK
* Gradio
* Pydantic
* python-dotenv
* JSON mock data
* Git and GitHub

## Project Structure

```text
agentic-holiday-planner/
│
├── app.py
├── README.md
├── requirements.txt
├── .env
├── .gitignore
│
├── travel_agents/
│   ├── request_parser_agent.py
│   ├── travel_manager.py
│   ├── flight_agent.py
│   ├── hotel_agent.py
│   ├── itinerary_agent.py
│   ├── budget_agent.py
│   └── booking_agent.py
│
├── tools/
│   ├── flight_tools.py
│   ├── hotel_tools.py
│   ├── itinerary_tools.py
│   ├── budget_tools.py
│   ├── booking_tools.py
│   └── recommendation_tools.py
│
├── models/
│   └── travel_request.py
│
├── memory/
│   └── session_memory.py
│
└── data/
    ├── mock_flights.json
    └── mock_hotels.json
```

## How It Works

1. The user enters a travel request.
2. The Request Parser Agent extracts structured trip details.
3. Session Memory stores user preferences.
4. The Travel Manager Agent coordinates specialist agents.
5. Flight and Hotel Agents search mock travel data.
6. Budget Agent checks if the trip fits the user's budget.
7. Itinerary Agent creates a simple day-by-day plan.
8. Booking Agent simulates booking only after user approval.

## Example Prompts

```text
I prefer nonstop flights and relaxed beach vacations.
```

```text
Plan a trip from Boston to Miami under $900.
```

```text
Yes, book the recommended option.
```

## Setup Instructions

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd agentic-holiday-planner
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Run the app:

```bash
python app.py
```

Open the Gradio local URL in your browser.

## Current Limitations

* Flight and hotel data are mock data.
* Booking is simulated only.
* No real payment is processed.
* No real flight or hotel reservation is made.
* Session memory resets when the app restarts.

## Future Improvements

* Add real flight and hotel search APIs.
* Add persistent SQLite memory.
* Add user profiles.
* Add real-time price comparison.
* Add booking links instead of simulated booking.
* Add map-based hotel recommendations.
* Add activity and restaurant planning agents.
* Add deployment using Hugging Face Spaces or Render.

## Disclaimer

This project is for educational and portfolio purposes. It does not make real bookings or payments.
