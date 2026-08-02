import os
import shutil
import uuid
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectResponse
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import run_project_pipeline
from app.dependencies import get_current_user
from app.models.user import User
from app.core.paths import GENERATED_PROJECTS_DIR

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = ProjectRepository(db)
    project = repo.create(current_user.id, project_data.name, project_data.idea_description)
    background_tasks.add_task(run_project_pipeline, str(project.id), project_data.idea_description)
    return project


@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = ProjectRepository(db)
    return repo.get_all_by_user(current_user.id)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = ProjectRepository(db)
    project = repo.get_by_id(project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/{project_id}/download")
def download_project(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = ProjectRepository(db)
    project = repo.get_by_id(project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")

    project_dir = os.path.join(GENERATED_PROJECTS_DIR, str(project_id))
    if not os.path.isdir(project_dir):
        raise HTTPException(status_code=404, detail="No generated files found for this project yet")

    zip_base_path = os.path.join(GENERATED_PROJECTS_DIR, f"{project_id}_archive")
    zip_path = shutil.make_archive(zip_base_path, "zip", project_dir)

    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in project.name)
    return FileResponse(
        zip_path,
        filename=f"{safe_name}.zip",
        media_type="application/zip",
    )
