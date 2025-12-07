import logging
from mcp.server.fastmcp import FastMCP
from typing import Optional
from data import FLIGHTS, HOTELS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


mcp = FastMCP("travel_planning_assistant")


@mcp.tool()
def search_flights(destination: str, budget: Optional[float] = None) -> str:
    """Search for flights to destination with optional budget filter."""
    logger.info(f"🔧 MCP TOOL CALLED: search_flights(destination={destination}, budget={budget})")
    try:
        if not destination:
            return "Error: Destination is required"

        # Filter by budget if provided
        flights = [f for f in FLIGHTS if budget is None or f['price'] <= budget]

        if not flights:
            budget_text = f" within £{budget} budget" if budget else ""
            return f"No flights found to {destination}{budget_text}"

        result = f"Flights to {destination}:\n"
        for flight in flights:
            result += f"- {flight['airline']}: £{flight['price']} at {flight['time']} ({flight['duration']}) - {flight['route']}\n"

        result += f"\nTotal options: {len(flights)}"
        if budget:
            result += f" (within £{budget} budget)"

        return result

    except Exception as e:
        return f"Error searching flights: {str(e)}"


@mcp.tool()
def search_hotels(city: str, budget: Optional[float] = None) -> str:
    """Search for hotels in city with optional budget filter."""
    logger.info(f"🔧 MCP TOOL CALLED: search_hotels(city={city}, budget={budget})")
    try:
        if not city:
            return "Error: City is required"

        # Filter by budget if provided
        hotels = [h for h in HOTELS if budget is None or h['price'] <= budget]

        if not hotels:
            budget_text = f" within £{budget} budget" if budget else ""
            return f"No hotels found in {city}{budget_text}"

        result = f"Hotels in {city}:\n"
        for hotel in hotels:
            amenities = ', '.join(hotel['amenities'])
            city_info = f" ({hotel['city']})" if hotel['city'] != city else ""
            result += f"- {hotel['name']}: £{hotel['price']}/night ({hotel['rating']} stars) - {amenities}{city_info}\n"

        result += f"\nTotal options: {len(hotels)}"
        if budget:
            result += f" (within £{budget} budget)"

        return result

    except Exception as e:
        return f"Error searching hotels: {str(e)}"


if __name__ == "__main__":
    logger.info("Starting Travel Planning MCP Server via stdio...")
    mcp.run(transport="stdio")
