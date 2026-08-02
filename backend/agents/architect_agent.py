from agents.base_agent import call_llm_json
from graphs.state import AgentState

SYSTEM_PROMPT = """You are a Software Architect AI agent. Given a list of requirements,
produce a concise system architecture plan.

Respond ONLY with valid JSON in this exact format, no markdown, no extra text:
{
  "frontend": "tech stack description",
  "backend": "tech stack description",
  "database": "database choice and reasoning",
  "folder_structure": "brief description of folder layout",
  "api_design": "brief description of key API endpoints needed"
}
"""


def architect_agent_node(state: AgentState) -> AgentState:
    result = call_llm_json(
        SYSTEM_PROMPT,
        f"Requirements: {state['requirements']}",
        temperature=0.3,
    )
    state["architecture_plan"] = result
    state["completed_steps"].append("architect_agent")
    state["messages"].append("[Architect Agent] Generated architecture plan.")
    return state
