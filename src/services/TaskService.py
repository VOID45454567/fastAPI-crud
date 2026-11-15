from sqlalchemy.orm import Session

from src.models.enums.TaskStatus import TaskStatus
from src.models.Task import Task

from src.entities.dto.task.create import TaskCreate
from src.entities.dto.task.update import TaskUpdate


def create(db: Session, user_id: int, data: TaskCreate) -> Task:
    task = Task(**data.model_dump(), user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get(db: Session, task_id: int) -> Task | None:
    return db.get(Task, task_id)


def list_(
    db: Session,
    *,
    user_id: int | None = None,
    status: TaskStatus | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Task]:
    q = db.query(Task)
    if user_id is not None:
        q = q.filter(Task.user_id == user_id)
    if status is not None:
        q = q.filter(Task.status == status)
    return q.order_by(Task.id).offset(skip).limit(limit).all()


def update(db: Session, task: Task, data: TaskUpdate) -> Task:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()