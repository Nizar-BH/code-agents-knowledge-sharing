"""
Investment Strategy Team - Analyzing NVIDIA Investment Decision
Four-agent team to provide comprehensive investment analysis
"""
from textwrap import dedent
from agno.agent import Agent
from agno.team.team import Team
from agno.tools.tavily import TavilyTools
from src.config.model_factory import ModelFactory

# Financial Analyst - Analyzes financial metrics and fundamentals
financial_analyst = Agent(
    name="Financial Analyst",
    role="Analyze financial metrics, revenue, profitability, and financial health",
    model=ModelFactory.create_model(),
    tools=[TavilyTools(
        enable_search=True,
        max_tokens=8000,
        search_depth="advanced",
        format="markdown"
    )],
    markdown=True,
    add_name_to_context=True,
    instructions=dedent("""
    Analyze NVIDIA's financial fundamentals:
    - Revenue growth trends and projections
    - Profitability metrics (margins, EPS, ROE)
    - Balance sheet strength (debt, cash position)
    - Valuation metrics (P/E, P/S, PEG ratios)
    - Recent earnings reports and guidance
    
    Provide quantitative analysis with specific metrics and comparisons to industry peers.
    Focus on financial health and growth sustainability.
    """),
)

# Market Analyst - Analyzes market position and competitive landscape
market_analyst = Agent(
    name="Market Analyst",
    role="Analyze market position, competition, and industry trends",
    model=ModelFactory.create_model(),
    tools=[TavilyTools(
        enable_search=True,
        max_tokens=8000,
        search_depth="advanced",
        format="markdown"
    )],
    markdown=True,
    add_name_to_context=True,
    instructions=dedent("""
    Evaluate NVIDIA's market position:
    - Market share in key segments (AI chips, data center, gaming)
    - Competitive landscape (AMD, Intel, custom chips)
    - Industry trends (AI adoption, data center growth, gaming market)
    - Competitive advantages and moats
    - Market opportunities and threats
    
    Assess competitive positioning and market dynamics.
    """),
)

# Technology Analyst - Analyzes technology trends and innovation
technology_analyst = Agent(
    name="Technology Analyst",
    role="Analyze technology trends, innovation, and product pipeline",
    model=ModelFactory.create_model(),
    tools=[TavilyTools(
        enable_search=True,
        max_tokens=8000,
        search_depth="advanced",
        format="markdown"
    )],
    markdown=True,
    add_name_to_context=True,
    instructions=dedent("""
    Evaluate NVIDIA's technology and innovation:
    - Product pipeline and roadmap (H100, Blackwell, next-gen architectures)
    - R&D investments and innovation capabilities
    - Technology leadership and patents
    - Partnerships and ecosystem (CUDA, AI frameworks)
    - Emerging technologies (quantum computing, edge AI, autonomous vehicles)
    
    Assess technological moat and innovation trajectory.
    """),
)

# Risk Analyst - Analyzes risks and potential downsides
risk_analyst = Agent(
    name="Risk Analyst",
    role="Identify risks, challenges, and potential downsides",
    model=ModelFactory.create_model(),
    tools=[TavilyTools(
        enable_search=True,
        max_tokens=8000,
        search_depth="advanced",
        format="markdown"
    )],
    markdown=True,
    add_name_to_context=True,
    instructions=dedent("""
    Identify investment risks and challenges:
    - Regulatory risks (export controls, trade restrictions)
    - Market risks (cyclicality, demand fluctuations)
    - Competitive risks (new entrants, technology shifts)
    - Execution risks (supply chain, manufacturing)
    - Valuation risks (overvaluation, market sentiment)
    
    Provide balanced risk assessment with probability and impact analysis.
    """),
)

# Investment Strategy Team - Coordinates all analysts
investment_team = Team(
    members=[
        financial_analyst,
        market_analyst,
        technology_analyst,
        risk_analyst,
    ],
    name="Investment Strategy Coordinator",
    model=ModelFactory.create_model(),
    delegate_to_all_members=False,
    description="Coordinate comprehensive investment analysis across four specialized analysts.",
    instructions=[
        "Workflow:",
        "1. Delegate to Financial Analyst to assess financial fundamentals",
        "2. Delegate to Market Analyst to evaluate competitive position",
        "3. Delegate to Technology Analyst to assess innovation and technology moat",
        "4. Delegate to Risk Analyst to identify potential downsides",
        "5. Synthesize all analyses into a comprehensive investment recommendation",
        "",
        "Output structure:",
        "- Executive Summary",
        "- Financial Analysis",
        "- Market Position Analysis",
        "- Technology & Innovation Assessment",
        "- Risk Assessment",
        "- Investment Recommendation (Buy/Hold/Sell) with rationale",
        "",
        "Provide clear, actionable investment advice based on all analyses.",
    ],
    add_datetime_to_context=True,
    share_member_interactions=True,
    show_members_responses=True,
    markdown=True,
)


if __name__ == "__main__":
    investment_team.print_response(
        "Should we invest in NVIDIA? Analyze the investment opportunity comprehensively. "
        "Consider a $100,000 investment horizon of 2-3 years.",
        stream=True,
        show_member_responses=True,
    )

