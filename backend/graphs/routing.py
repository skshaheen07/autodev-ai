from agents.supervisor_agent import AGENT_ORDER


def route_after_supervisor(state):
    next_agent = state.get("next_agent", "")
    if next_agent in AGENT_ORDER or next_agent == "healing_loop":
        return next_agent
    return "end"
