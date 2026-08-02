import uuid
from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    idea_description: str


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    idea_description: str
    status: str
    result: Dict[str, Any]
    created_at: datetime
