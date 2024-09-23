from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session

from ..entities.task import TaskEntity
from ..models.task import Task
from ..tools import uuid_generator
from ..utils.database import get_db_session

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}}
)

db_session = Annotated[Session, Depends(get_db_session)]
uuid = Annotated[str, Depends(uuid_generator)]


async def get_all_tasks():
    pass


async def create_new_task(
        new_task: TaskEntity,
        db_session: Session,
        uuid: str
):
    task = Task(id=uuid, text=new_task.text, datetime=new_task.created_at)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task.id


async def delete_task(
        task_id: str,
        db_session: Session
):
    task = db_session.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_session.delete(task)
    db_session.commit()

    return {
        "message": "Task with id " + task_id + " deleted successfully"
    }


async def edit_task(
        task_id: str,
        db_session: Session,
        text: str
):
    task = db_session.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.text=text
    db_session.commit()
    db_session.refresh(task)

    return {
        "message": "Task description with id " + task_id + " updated successfully"
    }


async def update_task_status(
        task_id: str,
        completed: bool,
        db_session: Session
):
    task = db_session.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = completed
    db_session.commit()
    db_session.refresh(task)

    return {
        "message": "Task status with id " + task_id + " updated successfully",
        "status": task.completed
    }


async def load_tasks(
        db_session: Session
):
    pass
