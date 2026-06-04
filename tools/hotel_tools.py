import json
from agents import function_tool
from services.serpapi_service import search_google_hotels


@function_tool
def search_hotels(
    city: str,
    max_price_per_night: int,
    check_in_date: str = "2026-07-10",
    check_out_date: str = "2026-07-13",
    adults: int = 1
) -> str:
    """
    Search real hotel options using SerpAPI Google Hotels.
    """

    results = search_google_hotels(
        destination=city,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        adults=adults
    )

    properties = results.get("properties", [])

    simplified_hotels = []

    for index, hotel in enumerate(properties[:10], start=1):
        rate_per_night = None

        rate_info = hotel.get("rate_per_night")

        if isinstance(rate_info, dict):
            rate_per_night = rate_info.get("extracted_lowest")

        if rate_per_night is None:
            total_rate = hotel.get("total_rate")

            if isinstance(total_rate, dict):
                rate_per_night = total_rate.get("extracted_lowest")

        if rate_per_night is None:
            continue

        if rate_per_night > max_price_per_night:
            continue

        simplified_hotels.append({
            "hotel_id": f"REAL_HOTEL_{index}",
            "name": hotel.get("name"),
            "price_per_night": rate_per_night,
            "rating": hotel.get("overall_rating"),
            "reviews": hotel.get("reviews"),
            "location_rating": hotel.get("location_rating"),
            "amenities": hotel.get("amenities", []),
            "link": hotel.get("link"),
            "type": "real_serpapi_google_hotels"
        })

    if not simplified_hotels:
        return "No real hotel options found within the nightly budget."

    return json.dumps(simplified_hotels[:5], indent=2)