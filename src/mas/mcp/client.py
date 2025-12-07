import asyncio
from textwrap import dedent
from agno.agent import Agent
from agno.team.team import Team
from agno.tools.mcp import MCPTools
from src.config.model_factory import ModelFactory

MCP_COMMAND = "uv run python src/mas/mcp/server.py"


async def plan_trip_with_team(travel_request: str):
    """Plan a trip using team approach with proper MCP connection management"""
    print("Team-Based Travel Planning Demo")
    print("=" * 60)

    # Keep MCP connection alive for the entire team execution
    # Increase timeout to 30 seconds to allow MCP server initialization
    async with MCPTools(MCP_COMMAND, timeout_seconds=30) as mcp_tools:

        # Create agents within the MCP context
        flight_specialist = Agent(
            name="Flight Specialist",
            role="Find flight options using custom booking system",
            model=ModelFactory.create_model(),
            tools=[mcp_tools],
            markdown=True,
            add_name_to_context=True,
            instructions=dedent("""
            You find flights from London to Tunisia using the search_flights tool.
            Focus on airlines like Tunisair, British Airways, EasyJet, and Ryanair with prices in British Pounds (£).

            YOU MUST ONLY PROVIDE FLIGHT INFORMATION.
            Do NOT provide hotel information.
            """),
        )

        hotel_specialist = Agent(
            name="Hotel Specialist",
            role="Find hotel options using custom booking system",
            model=ModelFactory.create_model(),
            tools=[mcp_tools],
            markdown=True,
            add_name_to_context=True,
            instructions=dedent("""
            You find Tunisian hotels using the search_hotels tool.
            Focus on hotels in Tunisia with prices in British Pounds (£) and local amenities.

            YOU MUST ONLY PROVIDE HOTEL INFORMATION.
            Do NOT provide flight information.
            """),
        )

        # Create team within the MCP context
        # AGNO 2.3.8 API Changes:

        # - enable_agentic_context removed
        travel_team = Team(
            members=[flight_specialist, hotel_specialist],
            name="Travel Planning Team",
            model=ModelFactory.create_model(),
            delegate_to_all_members=False, 
            description="Coordinate Tunisia travel booking using custom travel systems.",
            instructions=[
                "You coordinate flight and hotel booking from London to Tunisia with prices in British Pounds (£).",
                "1. Ask Flight Specialist to find flights from London to Tunisia",
                "2. Ask Hotel Specialist to find hotels in Tunisia",
                "3. Present complete travel plan with costs in British Pounds (£)",
            ],
            share_member_interactions=True,
            show_members_responses=True,
            markdown=True,
        )

        print(f"Travel Request: {travel_request}")
        print("-" * 60)

        # Execute team within the MCP context
        await travel_team.aprint_response(
            input=travel_request,
            stream=True,
        )


async def demo_travel_planning():
    """Demo the travel planning system"""
    print("Tunisia Travel Planning Team Demo with Custom MCP Server")
    provider = ModelFactory.get_provider()
    print(f"Using {provider.upper()}")
    print("=" * 65)

    travel_request = (
        "Plan a 5-day trip to Tunisia from London. "
        "Departure March 15th, return March 20th. "
        "Budget is £2000 total. "
        "Interested in traditional Tunisian culture, beaches, desert experiences, and local cuisine. "
        "Prefer destinations like Tunis, Djerba, Monastir, or Tozeur."
    )

    await plan_trip_with_team(travel_request)


if __name__ == "__main__":
    asyncio.run(demo_travel_planning())
