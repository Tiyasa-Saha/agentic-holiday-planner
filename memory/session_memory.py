import re


class SessionMemory:
    def __init__(self):
        self.preferences = {}

    def update_from_message(self, message: str):
        message_lower = message.lower()

        # Flight preference
        if "nonstop" in message_lower or "direct flight" in message_lower:
            self.preferences["flight_preference"] = "prefers nonstop/direct flights"

        # Travel style
        if "relaxed" in message_lower:
            self.preferences["travel_style"] = "relaxed"
        elif "adventure" in message_lower:
            self.preferences["travel_style"] = "adventure"
        elif "luxury" in message_lower:
            self.preferences["travel_style"] = "luxury"
        elif "budget" in message_lower:
            self.preferences["travel_style"] = "budget-friendly"

        # Beach preference
        if "beach" in message_lower:
            self.preferences["activity_preference"] = "likes beach activities"

        # Budget extraction
        budget_match = re.search(r"\$?(\d+)", message)
        if budget_match and ("budget" in message_lower or "under" in message_lower):
            self.preferences["budget"] = f"${budget_match.group(1)}"

        # Hotel budget extraction
        hotel_match = re.search(r"hotel.*?\$?(\d+)", message_lower)
        if hotel_match:
            self.preferences["hotel_budget"] = f"${hotel_match.group(1)} per night"

    def get_memory_summary(self) -> str:
        if not self.preferences:
            return "No saved user preferences yet."

        summary_lines = []

        for key, value in self.preferences.items():
            summary_lines.append(f"- {key}: {value}")

        return "\n".join(summary_lines)
    
    def save_selected_trip(self, flight_id: str, hotel_id: str):
        self.preferences["selected_flight_id"] = flight_id
        self.preferences["selected_hotel_id"] = hotel_id

    def has_selected_trip(self) -> bool:
        return (
            "selected_flight_id" in self.preferences
            and "selected_hotel_id" in self.preferences
        )

    def get_selected_trip(self) -> dict:
        return {
            "flight_id": self.preferences.get("selected_flight_id"),
            "hotel_id": self.preferences.get("selected_hotel_id"),
        }