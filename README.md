# AI Agents with Agno Framework

Production-ready AI agent implementations using Agno 2.3.8 with support for Ollama and OpenAI models.

## Project Structure

```
src/
├── config/
│   ├── model_factory.py      # Configurable LLM provider (Ollama/OpenAI)
│   └── __init__.py
├── mas/                       # Multi-Agent Systems
│   ├── investment_strategy.py # 4-agent investment analysis team
│   ├── hybrid_teams.py        # Hybrid architecture (parallel sub-team + sequential main team)
│   └── mcp/
│       ├── server.py          # MCP server with custom tools
│       ├── client.py          # MCP client with team coordination
│       └── data.py            # Sample data for MCP tools
├── memory_and_tools/
│   ├── agent_with_tools.py    # Agent with web search (Tavily)
│   ├── agent_with_stm.py      # Short-term memory (in-memory)
│   ├── agent_with_ltm.py      # Long-term memory (SQLite)
│   └── file_search_tool.py    # File search tool implementation
└── react_agent/
    └── agent_llamaindex.py    # ReAct agent with LlamaIndex
```

## Setup

### 1. Install UV

macOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install Dependencies

```bash
# Navigate to project directory
cd code-agents-knowledge-sharing

# Sync dependencies (creates virtual environment automatically)
uv sync
```

### 3. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:

**For Ollama (Local):**
```bash
MODEL_PROVIDER=ollama
OLLAMA_MODEL_ID=qwen3:8b
OLLAMA_TEMPERATURE=0.7
OLLAMA_API_KEY=
OLLAMA_HOST=http://localhost:11434
TAVILY_API_KEY=your_tavily_api_key_here
```

**For OpenAI:**
```bash
MODEL_PROVIDER=openai
OPENAI_MODEL_ID=gpt-4o
OPENAI_TEMPERATURE=0.7
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Install Ollama Models (if using Ollama)

```bash
# Install Ollama from https://ollama.ai
ollama pull qwen3:8b
```

## Running Examples

All commands should be run from the project root directory.

### Multi-Agent Systems

**Investment Strategy Team (4 agents):**
```bash
uv run python -m src.mas.investment_strategy
```

**Hybrid Architecture (Parallel Sub-Team + Sequential Main Team):**
```bash
uv run python -m src.mas.hybrid_teams
```

**MCP with Custom Tools:**
```bash
uv run python -m src.mas.mcp.client
```

### Memory & Tools

**Agent with Web Search:**
```bash
uv run python -m src.memory_and_tools.agent_with_tools
```

**Short-Term Memory (In-Memory):**
```bash
uv run python -m src.memory_and_tools.agent_with_stm
```

**Long-Term Memory (SQLite):**
```bash
uv run python -m src.memory_and_tools.agent_with_ltm
```

### ReAct Agent

**LlamaIndex ReAct Agent:**
```bash
uv run python -m src.react_agent.agent_llamaindex
```

## Key Features

### Model Factory
Centralized configuration for switching between Ollama and OpenAI:
- Set `MODEL_PROVIDER` in `.env`
- All agents automatically use the configured provider
- No code changes required to switch providers

### Multi-Agent Patterns

**Sequential Coordination** (`delegate_to_all_members=False`):
- Coordinator delegates tasks one agent at a time
- Each agent completes before the next starts
- Example: `investment_strategy.py`

**Parallel Execution** (`delegate_to_all_members=True`):
- All agents receive tasks simultaneously
- Work in parallel for diverse perspectives
- Example: Sub-team in `hybrid_teams.py`

### Memory Types

**Short-Term Memory (STM)**:
- In-memory storage (non-persistent)
- Maintains conversation history within session
- Use `InMemoryDb` for temporary context

**Long-Term Memory (LTM)**:
- Persistent SQLite storage
- Remembers across sessions
- Use `SqliteDb` with `enable_user_memories=True`

### MCP (Model Context Protocol)

Custom tools via MCP server:
- Define tools in `server.py`
- Agents access tools via `MCPTools`
- Works with stdio transport for proper initialization

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `MODEL_PROVIDER` | Yes | LLM provider | `ollama` or `openai` |
| `OLLAMA_MODEL_ID` | If using Ollama | Model identifier | `qwen3:8b` |
| `OLLAMA_TEMPERATURE` | If using Ollama | Temperature setting | `0.7` |
| `OLLAMA_API_KEY` | Only for Ollama Cloud | API key | Leave empty for local |
| `OLLAMA_HOST` | No | Ollama server URL | `http://localhost:11434` |
| `OPENAI_MODEL_ID` | If using OpenAI | Model identifier | `gpt-4o-mini` |
| `OPENAI_TEMPERATURE` | If using OpenAI | Temperature setting | `0.7` |
| `OPENAI_API_KEY` | If using OpenAI | OpenAI API key | `sk-...` |
| `TAVILY_API_KEY` | For web search | Tavily API key | Get from [tavily.com](https://tavily.com) |

## Troubleshooting

**MCP Connection Errors:**
- Ensure using `uv run python` (stdio transport) not `fastmcp run` (HTTP transport)
- Check server logs for tool call confirmations

**Ollama Connection:**
- Verify Ollama is running: `ollama list`
- Check host configuration in `.env`

**Import Errors:**
- Run `uv sync` to ensure dependencies are installed
- Always use `uv run python` to execute scripts

## Requirements

- Python 3.10+
- UV package manager
- Ollama (if using local models) or OpenAI API key
- Tavily API key (for web search features)