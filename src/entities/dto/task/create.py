from datetime import date

from pydantic import BaseModel

from src.models.enums.TaskStatus import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    priority: int
    due_date: date | None = None