from agents.base_agent import call_llm_json
from graphs.state import AgentState

SYSTEM_PROMPT = """You are a DevOps AI agent. Given an architecture plan, generate a
Dockerfile and docker-compose.yml suitable for this project.

Respond ONLY with valid JSON in this exact format, no markdown, no extra text:
{"deployment_config": {"Dockerfile": "content here", "docker-compose.yml": "content here"}}
"""


def devops_agent_node(state: AgentState) -> AgentState:
    result = call_llm_json(
        SYSTEM_PROMPT,
        f"Architecture: {state['architecture_plan']}",
        temperature=0.2,
    )
    state["deployment_config"] = result.get("deployment_config", {})
    state["completed_steps"].append("devops_agent")
    state["messages"].append("[DevOps Agent] Generated deployment configuration.")
    return state
