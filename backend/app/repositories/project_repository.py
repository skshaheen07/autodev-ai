import uuid
from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: uuid.UUID, name: str, idea_description: str) -> Project:
        project = Project(
            user_id=user_id,
            name=name,
            idea_description=idea_description,
            status="pending",
            result={},
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id) -> Project | None:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_all_by_user(self, user_id) -> list[Project]:
        return (
            self.db.query(Project)
            .filter(Project.user_id == user_id)
            .order_by(Project.created_at.desc())
            .all()
        )

    def update_status(self, project_id, status: str, result: dict | None = None) -> Project | None:
        project = self.get_by_id(project_id)
        if project:
            project.status = status
            if result is not None:
                project.result = result
            self.db.commit()
            self.db.refresh(project)
        return project
