from datetime import datetime
from sqlalchemy import Boolean, Column, String, DateTime
from ..utils.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(255), primary_key=True, unique=True)
    text = Column(String(255), default="")
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())

