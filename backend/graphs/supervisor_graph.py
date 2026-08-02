from langgraph.graph import StateGraph, END

from graphs.state import AgentState
from graphs.routing import route_after_supervisor
from agents.supervisor_agent import supervisor_node, AGENT_ORDER
from agents.product_agent import product_agent_node
from agents.architect_agent import architect_agent_node
from agents.database_agent import database_agent_node
from agents.backend_dev_agent import backend_dev_agent_node
from agents.frontend_dev_agent import frontend_dev_agent_node
from agents.reviewer_agent import reviewer_agent_node
from agents.testing_agent import testing_agent_node
from agents.docs_agent import docs_agent_node
from agents.devops_agent import devops_agent_node
from agents.healing_loop_agent import healing_loop_node

NODE_MAP = {
    "product_agent": product_agent_node,
    "architect_agent": architect_agent_node,
    "database_agent": database_agent_node,
    "backend_dev_agent": backend_dev_agent_node,
    "frontend_dev_agent": frontend_dev_agent_node,
    "reviewer_agent": reviewer_agent_node,
    "testing_agent": testing_agent_node,
    "docs_agent": docs_agent_node,
    "devops_agent": devops_agent_node,
}


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("healing_loop", healing_loop_node)
    for name, node_fn in NODE_MAP.items():
        workflow.add_node(name, node_fn)

    workflow.set_entry_point("supervisor")

    routing_map = {name: name for name in AGENT_ORDER}
    routing_map["end"] = END
    routing_map["healing_loop"] = "healing_loop"

    workflow.add_conditional_edges("supervisor", route_after_supervisor, routing_map)

    for name in AGENT_ORDER:
        workflow.add_edge(name, "supervisor")
    workflow.add_edge("healing_loop", "supervisor")

    return workflow.compile()
