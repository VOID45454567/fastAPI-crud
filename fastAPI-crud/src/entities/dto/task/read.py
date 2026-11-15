from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from src.models.enums.TaskStatus import TaskStatus

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: int
    due_date: date | None
    user_id: int
    created_at: datetime
    updated_at: datetime