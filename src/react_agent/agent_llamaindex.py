"""
ReAct Agent using LlamaIndex for multi-step research and report generation.
Demonstrates iterative reasoning: Think → Act → Observe → Think → Act...
"""
import os
import asyncio
from tavily import TavilyClient
from llama_index.core.agent.workflow import (
    ReActAgent,
    AgentStream,
    ToolCallResult
)
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_academic_programs(query: str) -> str:
    """
    Search for information about ENIT's academic programs.
    
    Args:
        query: Specific search query about academic programs
        
    Returns:
        Search results about academic programs
    """
    search_query = f"ENIT Tunis {query} academic programs engineering specializations"
    result = tavily_client.search(query=search_query, search_depth="advanced", max_results=5)
    
    formatted_results = []
    for item in result.get("results", []):
        formatted_results.append(
            f"- {item.get('title', 'N/A')}: {item.get('content', 'N/A')}\n"
            f"  Source: {item.get('url', 'N/A')}"
        )
    
    return "\n\n".join(formatted_results) if formatted_results else "No results found"


def search_research_innovation(query: str) -> str:
    """
    Search for information about ENIT's research and innovation activities.
    
    Args:
        query: Specific search query about research and innovation
        
    Returns:
        Search results about research and innovation
    """
    search_query = f"ENIT Tunis {query} research innovation projects laboratories"
    result = tavily_client.search(query=search_query, search_depth="advanced", max_results=5)
    
    formatted_results = []
    for item in result.get("results", []):
        formatted_results.append(
            f"- {item.get('title', 'N/A')}: {item.get('content', 'N/A')}\n"
            f"  Source: {item.get('url', 'N/A')}"
        )
    
    return "\n\n".join(formatted_results) if formatted_results else "No results found"


def search_rankings_reputation(query: str) -> str:
    """
    Search for information about ENIT's rankings and reputation.
    
    Args:
        query: Specific search query about rankings and reputation
        
    Returns:
        Search results about rankings and reputation
    """
    search_query = f"ENIT Tunis {query} rankings reputation international standing"
    result = tavily_client.search(query=search_query, search_depth="advanced", max_results=5)
    
    formatted_results = []
    for item in result.get("results", []):
        formatted_results.append(
            f"- {item.get('title', 'N/A')}: {item.get('content', 'N/A')}\n"
            f"  Source: {item.get('url', 'N/A')}"
        )
    
    return "\n\n".join(formatted_results) if formatted_results else "No results found"


def create_llm():
    """
    Create and return an LLM instance based on the MODEL_PROVIDER environment variable.
    
    Returns:
        LLM instance (OpenAI or Ollama)
    """
    provider = os.getenv("MODEL_PROVIDER", "openai").lower()
    
    if provider == "openai":
        model_id = os.getenv("OPENAI_MODEL_ID")
        if not model_id:
            raise ValueError("OPENAI_MODEL_ID environment variable is required")
        temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        return OpenAI(model=model_id, temperature=temperature)
    
    elif provider == "ollama":
        model_id = os.getenv("OLLAMA_MODEL_ID")
        if not model_id:
            raise ValueError("OLLAMA_MODEL_ID environment variable is required")
        temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
        return Ollama(model=model_id, temperature=temperature, request_timeout=120.0)
    
    else:
        raise ValueError(f"Unsupported provider: {provider}. Use 'openai' or 'ollama'")


async def main():
    provider = os.getenv("MODEL_PROVIDER", "openai").upper()
    print("=" * 100)
    print("ReAct-Style Agent (LlamaIndex): ENIT University Research Report")
    print(f"Provider: {provider}")
    print("=" * 100)
    
    llm = create_llm()
    
    tools = [
        FunctionTool.from_defaults(fn=search_academic_programs),
        FunctionTool.from_defaults(fn=search_research_innovation),
        FunctionTool.from_defaults(fn=search_rankings_reputation),
    ]
    
    agent = ReActAgent(
        tools=tools,
        llm=llm,
        system_prompt="""You are a research agent following the ReAct pattern.

MANDATORY FORMAT for your reasoning:
```
Thought: [What I need to do next and why]
Action: [The tool to call]
Action Input: [The input to the tool in JSON format]
```

Then after receiving results:
```
Observation: [What I learned from the tool results]
Thought: [What to do next based on this observation]
Action: [Next tool call, or FINISH if done]
```

Research workflow - work through ONE pillar at a time:
1. First use search_academic_programs to research Academic Programs
2. After observation, use search_research_innovation for Research & Innovation  
3. After observation, use search_rankings_reputation for Rankings & Reputation
4. After all observations, compile into a comprehensive report

RULES:
- Call tools ONE AT A TIME in the sequence above
- State OBSERVATION after EVERY tool result
- Make next THOUGHT based on OBSERVATION
- Work sequentially through all three pillars before final answer""",
    )
    
    query = """Create a comprehensive report about ENIT (École Nationale d'Ingénieurs de Tunis).

Research these three pillars:
1. Academic Programs - engineering programs and specializations
2. Research & Innovation - research strengths and notable projects  
3. Rankings & Reputation - national and international standing

For each pillar, search for information, then move to the next.
Finally, compile all findings into a cohesive report with clear sections."""
    
    print(f"\nTask: Research ENIT across 3 dimensions\n")
    print("-" * 100)
    
    handler = agent.run(user_msg=query)
    
    async for event in handler.stream_events():
        if isinstance(event, ToolCallResult):
            print(f"\n{'=' * 80}")
            print(f"TOOL: {event.tool_name}")
            print(f"INPUT: {event.tool_kwargs}")
            print(f"{'=' * 80}\n")
        elif isinstance(event, AgentStream):
            print(f"{event.delta}", end="", flush=True)
    
    response = await handler
    
    print("\n" + "=" * 100)
    print("FINAL RESPONSE:")
    print("=" * 100)
    print(str(response))


if __name__ == "__main__":
    asyncio.run(main())
