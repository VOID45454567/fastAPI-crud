from datetime import datetime
from enum import Enum
import enum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.connect import Base


class TaskStatus(enum.Enum): 
    TODO="todo",
    ON_COMLETE="on_comlete",
    COMLETED="comleted"


class Task(Base): 
    
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name ="status", default=TaskStatus.TODO)
    )
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    
    user = relationship("User", back_populates="tasks")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    