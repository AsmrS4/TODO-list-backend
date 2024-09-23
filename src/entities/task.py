from datetime import datetime
from pydantic import BaseModel

class TaskEntity(BaseModel):
    text: str
    completed: bool
    created_at: datetime
