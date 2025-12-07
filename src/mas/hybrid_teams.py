"""
Hybrid Team Architecture - Startup Due Diligence
Demonstrates parallel execution within a sub-team + sequential coordination at main team level
"""
from textwrap import dedent
from agno.agent import Agent
from agno.team.team import Team
from agno.tools.tavily import TavilyTools
from src.config.model_factory import ModelFactory

# Technical Assessment Sub-Team - Multiple experts assess in parallel

backend_architect = Agent(
    name="Backend Architect",
    role="Assess backend architecture, scalability, and technical debt",
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
    Evaluate the startup's backend technical stack:
    - Architecture design and scalability
    - Database design and data management
    - API design and microservices
    - Code quality and technical debt
    - Performance and optimization
    - Security practices
    
    Provide technical assessment with specific findings and recommendations.
    """),
)

frontend_architect = Agent(
    name="Frontend Architect",
    role="Assess frontend architecture, UX, and performance",
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
    Evaluate the startup's frontend technical stack:
    - Frontend framework and architecture
    - User experience and interface design
    - Performance and loading times
    - Mobile responsiveness
    - Accessibility standards
    - Code maintainability
    
    Provide frontend assessment with specific findings and recommendations.
    """),
)

infrastructure_architect = Agent(
    name="Infrastructure Architect",
    role="Assess infrastructure, DevOps, and operational practices",
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
    Evaluate the startup's infrastructure and operations:
    - Cloud infrastructure and architecture
    - DevOps practices and CI/CD pipelines
    - Monitoring and observability
    - Disaster recovery and backup
    - Cost optimization
    - Security and compliance
    
    Provide infrastructure assessment with specific findings and recommendations.
    """),
)

# Technical Assessment Sub-Team - Executes in parallel for comprehensive technical review
technical_assessment_team = Team(
    members=[
        backend_architect,
        frontend_architect,
        infrastructure_architect,
    ],
    name="Technical Assessment Team",
    model=ModelFactory.create_model(),
    delegate_to_all_members=True,  # Parallel execution - all architects assess simultaneously
    description="Technical experts assess different aspects of the tech stack in parallel.",
    instructions=[
        "Each architect independently assesses their domain.",
        "Provide comprehensive technical evaluation from your perspective.",
        "Work in parallel to gather diverse technical insights.",
    ],
    markdown=True,
)

# Business Analyst - Evaluates business viability
business_analyst = Agent(
    name="Business Analyst",
    role="Assess business model, market fit, and growth potential",
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
    Evaluate the startup's business viability:
    - Business model and revenue streams
    - Market opportunity and competition
    - Product-market fit
    - Growth trajectory and metrics
    - Team and execution capability
    - Financial sustainability
    
    Provide business assessment with market analysis and growth potential.
    """),
)

# Main Due Diligence Committee - Coordinates sub-team and business analyst
due_diligence_committee = Team(
    members=[
        technical_assessment_team,  # Sub-team with parallel execution
        business_analyst,  # Individual analyst
    ],
    name="Due Diligence Committee",
    model=ModelFactory.create_model(),
    delegate_to_all_members=False,  # Sequential coordination at main level
    description="Main committee coordinating technical assessment sub-team and business analysis.",
    instructions=[
        "Workflow:",
        "1. Delegate to Technical Assessment Team to evaluate tech stack in parallel",
        "   - Backend, Frontend, and Infrastructure architects work simultaneously",
        "2. Delegate to Business Analyst to assess business viability",
        "3. Synthesize all assessments into investment decision",
        "",
        "Output structure:",
        "- Technical Assessment Summary",
        "  - Backend findings",
        "  - Frontend findings",
        "  - Infrastructure findings",
        "- Business Assessment",
        "- Overall Risk Analysis",
        "- Investment Recommendation (Invest/Pass/Further Investigation)",
        "- Key Decision Factors",
        "",
        "Provide clear, actionable investment recommendation based on all assessments.",
    ],
    add_datetime_to_context=True,
    share_member_interactions=True,
    show_members_responses=True,
    markdown=True,
)


if __name__ == "__main__":
    due_diligence_committee.print_response(
        "We're considering a $5M Series A investment in a SaaS startup. "
        "The company is TechFlow, an AI-powered project management tool with 10K users. "
        "Conduct comprehensive due diligence: technical assessment and business viability. "
        "Tech stack: Python/FastAPI backend, React frontend, AWS infrastructure.",
        stream=True,
        show_member_responses=True,
    )

