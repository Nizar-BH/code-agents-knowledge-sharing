from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from src.config.model_factory import ModelFactory


if __name__ == '__main__':

    query = "What are the latest trends in AI for 2025?"

    # Simple agent with web search tool
    # - search=True → enable_search=True (TavilyTools)
    agent = Agent(
        model=ModelFactory.create_model(),
        tools=[
            TavilyTools(
                enable_search=True,
                max_tokens=8000,
                search_depth="advanced",
                format="markdown"
            )
        ],
        markdown=True
    )

    agent.print_response(query, stream=True)
