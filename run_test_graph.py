import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from graphs.supervisor_graph import build_graph

if __name__ == "__main__":
    graph = build_graph()

    initial_state = {
        "project_id": "test-001",
        "user_request": "Build a simple expense tracker web app",
        "requirements": [],
        "architecture_plan": {},
        "generated_files": {},
        "review_report": {},
        "test_report": {},
        "documentation": "",
        "deployment_config": {},
        "messages": [],
        "next_agent": "",
        "status": "in_progress",
        "retry_count": 0,
        "completed_steps": [],
    }

    final_state = graph.invoke(initial_state, config={"recursion_limit": 50})

    print("\n=== AGENT CONVERSATION LOG ===")
    for msg in final_state["messages"]:
        print(msg)

    print("\n=== COMPLETED STEPS ===")
    print(final_state["completed_steps"])
