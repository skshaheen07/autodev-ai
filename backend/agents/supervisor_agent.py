import json

from agents.base_agent import get_llm, _invoke_with_backoff
from graphs.state import AgentState

AGENT_ORDER = [
    "product_agent",
    "architect_agent",
    "database_agent",
    "backend_dev_agent",
    "frontend_dev_agent",
    "reviewer_agent",
    "testing_agent",
    "docs_agent",
    "devops_agent",
]

MAX_HEALING_RETRIES = 1

SUPERVISOR_SYSTEM_PROMPT = """You are the Supervisor Agent coordinating a 9-agent AI
software engineering team. Agents must run in this order, skipping any already completed:

1. product_agent
2. architect_agent
3. database_agent
4. backend_dev_agent
5. frontend_dev_agent
6. reviewer_agent
7. testing_agent
8. docs_agent
9. devops_agent

If all are completed, respond with "end".

Respond ONLY with valid JSON, no markdown, no extra text:
{"next_agent": "<agent_name_or_end>", "reasoning": "<one short sentence>"}
"""


def _determine_next_agent_from_state(state: AgentState) -> str:
    completed = set(state.get("completed_steps", []))

    test_report = state.get("test_report", {})
    healing_attempts = state.get("retry_counts", {}).get("healing_loop", 0)

    if (
        "testing_agent" in completed
        and test_report.get("passed") is False
        and healing_attempts < MAX_HEALING_RETRIES
    ):
        return "healing_loop"

    for agent_name in AGENT_ORDER:
        if agent_name not in completed:
            return agent_name
    return "end"


def supervisor_node(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0)

    completed = state.get("completed_steps", [])
    prompt = (
        f"{SUPERVISOR_SYSTEM_PROMPT}\n\n"
        f"Completed agents so far: {completed}\n"
    )

    response = _invoke_with_backoff(llm, prompt)
    content = response.content.strip()

    try:
        decision = json.loads(content)
        llm_next = decision.get("next_agent", "end")
        reasoning = decision.get("reasoning", "")
    except json.JSONDecodeError:
        llm_next = "end"
        reasoning = "Could not parse supervisor response."

    correct_next = _determine_next_agent_from_state(state)

    if correct_next == "healing_loop":
        reasoning = "Tests failed - routing back to backend_dev_agent to fix issues before proceeding."
    elif llm_next != correct_next:
        reasoning += f" (corrected: LLM suggested '{llm_next}', overridden to '{correct_next}' based on completed_steps check.)"

    state["next_agent"] = correct_next
    state["messages"].append(f"[Supervisor] {reasoning}")
    return state
