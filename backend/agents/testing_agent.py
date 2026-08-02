from agents.base_agent import call_llm_json
from graphs.state import AgentState

SYSTEM_PROMPT = """You are a Testing AI agent. Given generated code files, describe what
tests would validate them and simulate whether the code would pass basic checks
(syntax sanity, obvious logic errors).

Respond ONLY with valid JSON in this exact format, no markdown, no extra text:
{
  "passed": true,
  "results": ["test description: pass/fail reasoning", "..."]
}
"""


def testing_agent_node(state: AgentState) -> AgentState:
    files_summary = {path: content[:500] for path, content in state["generated_files"].items()}
    result = call_llm_json(
        SYSTEM_PROMPT,
        f"Generated files (truncated):\n{files_summary}",
        temperature=0.2,
    )
    state["test_report"] = result
    state["completed_steps"].append("testing_agent")
    state["messages"].append(
        f"[Testing Agent] Testing complete. Passed: {result.get('passed', 'unknown')}."
    )
    return state
