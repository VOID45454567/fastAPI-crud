from datetime import date

from pydantic import BaseModel

from src.models.enums.TaskStatus import TaskStatus


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: int | None = None
    due_date: date | None = None