from datetime import date
from typing import Optional, List
from pydantic import BaseModel


class TaskEntity(BaseModel):
    id: Optional[str]
    text: Optional[str] = None
    completed: Optional[bool] = None
    created_at: Optional[date] = None


class TaskList(BaseModel):
    tasks: Optional[List[TaskEntity]] = None
