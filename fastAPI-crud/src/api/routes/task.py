from fastapi import APIRouter, HTTPException

from src.models.enums.TaskStatus import TaskStatus
from src.api.deps import SessionDep
from src.services import TaskService as crud_task
from src.services import UserService as crud_user
from src.entities.dto.task.create import TaskCreate
from src.entities.dto.task.read import TaskRead
from src.entities.dto.task.update import TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead, status_code=201)
def create_task(user_id: int, data: TaskCreate, db: SessionDep):
    if not crud_user.get(db, user_id):
        raise HTTPException(404, "User not found")
    return crud_task.create(db, user_id, data)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    db: SessionDep,
    user_id: int | None = None,
    status: TaskStatus | None = None,
    skip: int = 0,
    limit: int = 100,
):
    return crud_task.list_(db, user_id=user_id, status=status, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: SessionDep):
    task = crud_task.get(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, data: TaskUpdate, db: SessionDep):
    task = crud_task.get(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return crud_task.update(db, task, data)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: SessionDep):
    task = crud_task.get(db, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    crud_task.delete(db, task)