from agents.base_agent import call_llm_json
from graphs.state import AgentState

SYSTEM_PROMPT = """You are a senior Code Reviewer AI agent. Review the given generated
files for bugs, security issues, and code quality problems.

Respond ONLY with valid JSON in this exact format, no markdown, no extra text:
{
  "issues": ["issue 1", "issue 2"],
  "severity": "low|medium|high",
  "approved": true
}
"""


def reviewer_agent_node(state: AgentState) -> AgentState:
    files_summary = {path: content[:500] for path, content in state["generated_files"].items()}
    result = call_llm_json(
        SYSTEM_PROMPT,
        f"Generated files (truncated):\n{files_summary}",
        temperature=0.2,
    )
    state["review_report"] = result
    state["completed_steps"].append("reviewer_agent")
    state["messages"].append(
        f"[Reviewer Agent] Review complete. Approved: {result.get('approved', 'unknown')}."
    )
    return state
