from graphs.state import AgentState


def healing_loop_node(state: AgentState) -> AgentState:
    retry_counts = state.get("retry_counts", {})
    retry_counts["healing_loop"] = retry_counts.get("healing_loop", 0) + 1
    state["retry_counts"] = retry_counts

    test_report = state.get("test_report", {})
    failure_summary = "; ".join(test_report.get("results", [])) or "Tests failed."

    state.setdefault("last_failure_reason", {})["backend_dev_agent"] = (
        f"Testing Agent reported failures: {failure_summary}"
    )

    # Remove backend_dev_agent and testing_agent from completed so they run again
    state["completed_steps"] = [
        step for step in state["completed_steps"]
        if step not in ("backend_dev_agent", "testing_agent")
    ]

    state["messages"].append(
        "[Self-Healing] Sending backend_dev_agent back to fix issues found by Testing Agent."
    )
    return state
