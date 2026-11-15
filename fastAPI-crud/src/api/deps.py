from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.connect import get_db

SessionDep = Annotated[Session, Depends(get_db)]