from pydantic import BaseModel


class TravelRequest(BaseModel):
    origin: str
    destination: str
    budget: int
    number_of_days: int
    number_of_nights: int
    number_of_travelers: int
    hotel_budget_per_night: int
    travel_style: str
    flight_preference: str
    activity_preference: str