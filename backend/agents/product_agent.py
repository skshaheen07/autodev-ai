from agents.base_agent import call_llm_json
from graphs.state import AgentState

SYSTEM_PROMPT = """You are a Product Manager AI agent. Convert a raw software idea into a
concise list of 4-6 concrete features/requirements needed to build it.

Respond ONLY with valid JSON in this exact format, no markdown, no extra text:
{"requirements": ["requirement 1", "requirement 2", ...]}
"""


def product_agent_node(state: AgentState) -> AgentState:
    result = call_llm_json(
        SYSTEM_PROMPT,
        f"User's idea: {state['user_request']}",
        temperature=0.4,
    )
    requirements = result.get("requirements", [])
    state["requirements"] = requirements
    state["completed_steps"].append("product_agent")
    state["messages"].append(f"[Product Agent] Generated {len(requirements)} requirements.")
    return state
