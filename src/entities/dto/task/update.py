from pydantic import BaseModel


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: int | None = None