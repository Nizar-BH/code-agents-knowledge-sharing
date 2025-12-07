from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from src.memory_and_tools.file_search_tool import file_search_tool
from src.config.model_factory import ModelFactory


if __name__ == '__main__':

    query_storage = "Do your remember the contents of the pyproject.toml file and return all of its content"
    # query = "search for the pyproject.toml file and return all of its content"

    # AGNO 2.3.8 - Long-Term Memory (LTM)
    # Long-term memory stores persistent user memories across sessions
    # Key features:
    # - enable_user_memories=True: Creates/updates user memories after each run
    # - db: Required for storing memories persistently
    # - user_id: Required to associate memories with specific users
    # - add_history_to_context: Adds conversation history within session
    # Model provider configured via MODEL_PROVIDER env var (ollama or openai)
    agent = Agent(
        model=ModelFactory.create_model(),
        user_id="demo_user",  # Required for user memories
        session_id="demo_ltm_session",
        db=SqliteDb(
            session_table="agent_sessions",
            db_file="tmp_dbs/demo_ltm.db"
        ),
        enable_user_memories=True,  # Enable long-term memory (persistent user memories)
        add_history_to_context=True,  # Short-term memory (conversation history)
        num_history_runs=3,
        tools=[file_search_tool],
        markdown=True
    )

    agent.print_response(query_storage, stream=True)
    # agent.print_response(query, stream=True)
