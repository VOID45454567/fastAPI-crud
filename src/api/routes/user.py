from fastapi import APIRouter, HTTPException

from src.api.deps import SessionDep
from src.services import TaskService as crud_task
from src.services import UserService as crud_user
from src.entities.dto.task.read import TaskRead
from src.entities.dto.user.create import UserCreate
from src.entities.dto.user.read import UserRead
from src.entities.dto.user.update import UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=201)
def create_user(data: UserCreate, db: SessionDep):
    if crud_user.get_by_email(db, data.email):
        raise HTTPException(409, "Email already registered")
    return crud_user.create(db, data)


@router.get("", response_model=list[UserRead])
def list_users(db: SessionDep, skip: int = 0, limit: int = 100):
    return crud_user.list_(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: SessionDep):
    user = crud_user.get(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, db: SessionDep):
    user = crud_user.get(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return crud_user.update(db, user, data)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: SessionDep):
    user = crud_user.get(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    crud_user.delete(db, user)


@router.get("/{user_id}/tasks", response_model=list[TaskRead])
def list_user_tasks(user_id: int, db: SessionDep):
    if not crud_user.get(db, user_id):
        raise HTTPException(404, "User not found")
    return crud_task.list_(db, user_id=user_id)