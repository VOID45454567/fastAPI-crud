from datetime import date

from pydantic import BaseModel


class TaskCreate(BaseModel): 
    title: str
    description: str | None = None
    status: str = "todo"
    priority: int
    due_date: date | None = None