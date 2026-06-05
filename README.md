# Agentic Holiday Planner

An AI-powered multi-agent travel planning system built using the PRMA (Plan, Reason, Memory, Act) framework.

The application helps users plan trips, compare real flights and hotels, generate itineraries, remember travel preferences, and simulate bookings through a conversational interface.

## Features

### Real Travel Search

* Real flight search using SerpAPI Google Flights
* Real hotel search using SerpAPI Google Hotels
* Destination research using OpenAI web search
* Budget-aware trip recommendations

### Multi-Agent Architecture

The system is composed of specialized agents:

* Request Parser Agent
* Travel Manager Agent
* Flight Search Agent
* Hotel Search Agent
* Destination Research Agent
* Booking Agent

Each agent has a dedicated responsibility and collaborates to generate the final travel recommendation.

### PRMA Framework

#### Plan

Parses user travel requests and extracts:

* Origin
* Destination
* Budget
* Travel dates
* Travel preferences

#### Reason

Compares:

* Flights
* Hotels
* Budget constraints
* Travel preferences

Generates personalized recommendations.

#### Memory

Supports:

* Session memory
* Persistent SQLite memory
* Multi-user preference profiles

User preferences can be saved and reused across sessions.

#### Act

Performs:

* Flight search
* Hotel search
* Destination research
* Simulated booking

No real bookings or payments are processed.

## Preference Management

Users can save preferences such as:

* Flight preference

  * Nonstop
  * Cheapest
  * Shortest duration

* Travel style

  * Relaxed
  * Luxury
  * Adventure
  * Budget-friendly

* Activity preference

  * Beach
  * Food
  * Nature
  * Nightlife
  * Culture

* Hotel budget

* Total trip budget

Preferences are stored in SQLite and persist across application restarts.

## Technology Stack

### Frontend

* Gradio

### LLM Framework

* OpenAI Agents SDK
* OpenAI GPT models

### Travel Data

* SerpAPI Google Flights
* SerpAPI Google Hotels

### Storage

* SQLite
* Session Memory

### Language

* Python

## Project Structure

```text
agentic-holiday-planner/
│
├── app.py
│
├── travel_agents/
│   ├── request_parser_agent.py
│   ├── travel_manager.py
│   ├── flight_agent.py
│   ├── hotel_agent.py
│   ├── booking_agent.py
│   └── destination_research_agent.py
│
├── tools/
│   ├── flight_tools.py
│   ├── hotel_tools.py
│   ├── booking_tools.py
│   └── web_research_tools.py
│
├── services/
│   └── serpapi_service.py
│
├── memory/
│   ├── session_memory.py
│   ├── sqlite_memory.py
│   └── user_preferences.db
│
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## Setup

### Clone Repository

```bash
git clone <repository-url>
cd agentic-holiday-planner
```

### Create Virtual Environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key

SERPAPI_API_KEY=your_serpapi_api_key
SERPAPI_BASE_URL=https://serpapi.com/search
```

### Run Application

```powershell
python app.py
```

## Example Workflow

User:

```text
Plan a trip from Boston to Miami under $900.
```

System:

```text
✓ Search real flights
✓ Search real hotels
✓ Check budget
✓ Generate itinerary
✓ Recommend best option
```

User:

```text
Yes, simulate booking this option.
```

System:

```text
✓ Retrieve latest recommended flight and hotel
✓ Simulate booking
✓ Generate booking confirmation
```

## Current Capabilities

* Real flight search
* Real hotel search
* Persistent user preferences
* Multi-user support
* Budget-aware recommendations
* Destination research
* Simulated booking workflow
* PRMA-based agent orchestration

## Future Enhancements

* Personalized recommendation scoring engine
* PRMA dashboard visualization
* Trip history
* Real booking links
* Calendar integration
* Multi-destination trip planning
* Travel alerts and price tracking

## Disclaimer

This project is for educational and portfolio purposes.

Flight and hotel searches use real travel data sources. However, bookings remain simulated and no real reservations or payments are made.
