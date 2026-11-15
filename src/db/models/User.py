from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.connect import Base



class User(Base):
    
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    
    
    login: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    
    tasks = relationship("Task", back_populates="user")