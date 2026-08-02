from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    project_id: str
    user_request: str
    requirements: List[str]
    architecture_plan: Dict[str, Any]
    generated_files: Dict[str, str]
    review_report: Dict[str, Any]
    test_report: Dict[str, Any]
    documentation: str
    deployment_config: Dict[str, str]
    messages: List[str]
    next_agent: str
    status: str
    retry_count: int
    completed_steps: List[str]
    retry_counts: Dict[str, int]
    last_failure_reason: Dict[str, str]
