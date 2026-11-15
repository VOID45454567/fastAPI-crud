from pydantic import BaseModel


class UserUpdate(BaseModel):
    login: str | None = None
    email: str | None = None