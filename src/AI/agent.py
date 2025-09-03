from pydantic_ai import Agent, Tool, RunContext
from schemas.agent import AgentResponse

agent = Agent[AgentResponse](
    model="gpt-4o-mini",
    system_prompt="""
    You are Tessa AI support assistant.
    Answer user support tickets in a professional, concise way.
    Always include a confidence score between 0 and 10 in your reasoning.
    """,
)

@agent.tool
def escalate_ticket(ctx: RunContext, ticket_id: int) -> str:
    """Escalate a ticket to a human sub-admin."""
    # You’d actually update your DB here
    return f"Ticket {ticket_id} has been escalated to a human."