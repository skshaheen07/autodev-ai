import os

from app.db.session import SessionLocal
from app.repositories.project_repository import ProjectRepository
from app.core.paths import GENERATED_PROJECTS_DIR


def _write_files_to_disk(project_id: str, files: dict) -> None:
    project_dir = os.path.join(GENERATED_PROJECTS_DIR, project_id)
    os.makedirs(project_dir, exist_ok=True)

    for relative_path, content in files.items():
        safe_relative_path = relative_path.lstrip("/\\")
        full_path = os.path.join(project_dir, safe_relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)


def run_project_pipeline(project_id: str, user_request: str) -> None:
    from graphs.supervisor_graph import build_graph

    db = SessionLocal()
    repo = ProjectRepository(db)
    try:
        repo.update_status(project_id, "in_progress")

        graph = build_graph()
        initial_state = {
            "project_id": project_id,
            "user_request": user_request,
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
            "retry_counts": {},
            "last_failure_reason": {},
        }

        final_state = graph.invoke(initial_state, config={"recursion_limit": 50})

        all_files = dict(final_state["generated_files"])
        if final_state.get("documentation"):
            all_files["README.md"] = final_state["documentation"]
        for fname, fcontent in final_state.get("deployment_config", {}).items():
            all_files[fname] = fcontent

        _write_files_to_disk(project_id, all_files)

        result = {
            "requirements": final_state["requirements"],
            "architecture_plan": final_state["architecture_plan"],
            "generated_files": final_state["generated_files"],
            "review_report": final_state["review_report"],
            "test_report": final_state["test_report"],
            "documentation": final_state["documentation"],
            "deployment_config": final_state["deployment_config"],
            "messages": final_state["messages"],
            "completed_steps": final_state["completed_steps"],
            "retry_counts": final_state["retry_counts"],
        }

        repo.update_status(project_id, "completed", result)
    except Exception as e:
        repo.update_status(project_id, "failed", {"error": str(e)})
    finally:
        db.close()
