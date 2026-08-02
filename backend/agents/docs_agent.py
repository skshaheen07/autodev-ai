from agents.base_agent import get_llm
from graphs.state import AgentState

SYSTEM_PROMPT = """You are a Documentation AI agent. Write a concise README.md for this
project, covering: project overview, features, tech stack, and setup instructions.
Respond with the raw markdown content only, no extra commentary."""


def docs_agent_node(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0.4)
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Project idea: {state['user_request']}\n"
        f"Requirements: {state['requirements']}\n"
        f"Architecture: {state['architecture_plan']}\n"
    )
    response = llm.invoke(prompt)
    state["documentation"] = response.content
    state["completed_steps"].append("docs_agent")
    state["messages"].append("[Docs Agent] Generated README documentation.")
    return state
