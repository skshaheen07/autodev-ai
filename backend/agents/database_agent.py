import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from agents.base_agent import call_llm_files
from graphs.state import AgentState
from tools.rag_retriever_tool import retrieve_context

SYSTEM_PROMPT = """You are a Database Engineer AI agent. Given requirements and an
architecture plan, design a SQL schema (CREATE TABLE statements) for a PostgreSQL database.
Output it as a single file at path database/schema.sql."""

MAX_RETRIES = 2


def database_agent_node(state: AgentState) -> AgentState:
    retry_counts = state.get("retry_counts", {})
    attempt = retry_counts.get("database_agent", 0)

    query = "SQL database schema " + " ".join(state["requirements"])
    retrieved = retrieve_context(query, category="database", n_results=2)
    context_block = "\n".join(f"- {r}" for r in retrieved)

    user_content = (
        f"Requirements: {state['requirements']}\n"
        f"Architecture: {state['architecture_plan']}\n\n"
        f"Relevant best practices to follow:\n{context_block}"
    )

    previous_failure = state.get("last_failure_reason", {}).get("database_agent")
    if previous_failure:
        user_content += (
            f"\n\nNOTE: A previous attempt failed with this issue: {previous_failure}\n"
            "Make sure to follow the exact output format this time."
        )

    result = call_llm_files(SYSTEM_PROMPT, user_content, temperature=0.2)
    files = result.get("files", {})

    if not files and attempt < MAX_RETRIES:
        retry_counts["database_agent"] = attempt + 1
        state["retry_counts"] = retry_counts
        state.setdefault("last_failure_reason", {})["database_agent"] = (
            "No files were generated - output format was not followed correctly."
        )
        state["messages"].append(
            f"[Database Agent] Attempt {attempt + 1} produced 0 files. Retrying..."
        )
        return database_agent_node(state)

    state["generated_files"].update(files)
    state["completed_steps"].append("database_agent")
    state["messages"].append(
        f"[Database Agent] Generated {len(files)} schema file(s) using {len(retrieved)} "
        f"retrieved best-practice references (attempt {attempt + 1})."
    )
    return state
