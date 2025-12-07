from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.db.in_memory import InMemoryDb
from src.memory_and_tools.file_search_tool import file_search_tool
from src.config.model_factory import ModelFactory


if __name__ == '__main__':

    query_one = "search for the pyproject.toml file and return all of its content"
    query_two = "What are the latest papers released related to LLM Agents"


    # AGNO 2.3.8 - Short-Term Memory (STM) with In-Memory Storage
    # Short-term memory maintains conversation history within the current session only
    # Key features:
    # - add_history_to_context=True: Adds previous conversation to context
    # - num_history_runs=3: Includes last 3 conversation turns
    # - InMemoryDb: Stores session data in memory (non-persistent, cleared when script ends)
    # Note: This is in-memory storage - data is NOT saved to disk and is lost when the script ends
    agent = Agent(
        model=ModelFactory.create_model(),
        db=InMemoryDb(),  # In-memory storage (non-persistent)
        tools=[
            TavilyTools(
                enable_search=True,
                max_tokens=8000,
                search_depth="advanced",
                format="markdown"
            ),
            file_search_tool
        ],
        add_history_to_context=True,  # Enable short-term memory (conversation history)
        num_history_runs=2,  # Include last 2 conversation turns
        markdown=True
    )

    agent.print_response(query_one, stream=True)
    agent.print_response(query_two, stream=True)
    agent.print_response("What was the content of the pyproject.toml file? dont use any tool.")
