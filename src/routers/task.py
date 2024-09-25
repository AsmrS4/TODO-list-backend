from typing import Annotated, List
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from src.utils.database import Base, engine, get_db_session
from src.entities.task import TaskEntity
from src.models.task import Task
from src.tools.uuid_generator import uuid_generator


router = APIRouter(
    prefix="/api/task",
    tags=["task"],
    responses={404: {"description": "Not found"}}
)

Base.metadata.create_all(bind=engine)

db_session = Annotated[Session, Depends(get_db_session)]
get_uuid = Annotated[str, Depends(uuid_generator)]


@router.get("/")
async def get_all_tasks(
        db: db_session,
) -> List[TaskEntity]:
    result = db.query(Task).all()
    return result


@router.post("/new")
async def create_new_task(
        db: db_session,
        uuid: get_uuid,
        text: str | None = None

) -> str:
    task = Task(id=uuid, text=text)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task.id


@router.delete("/delete/{task_id}")
async def delete_task(
        db: db_session,
        task_id: str
):

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return JSONResponse({
        "message": "Task with id " + task_id + " deleted successfully"
    })


@router.put("/edit/{task_id}")
async def edit_task(
        db: db_session,
        task_id: str,
        text: str | None = None
) -> JSONResponse:

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.text = text
    db.commit()
    db.refresh(task)

    return JSONResponse({
        "message": "Task description with id " + task_id + " updated successfully"
    })


@router.post("/{task_id}/status")
async def update_task_status(
        db: db_session,
        task_id: str,
        completed: bool
) -> str:

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = completed
    db.commit()
    db.refresh(task)

    return JSONResponse({
        "message": "Task status with id " + task_id + " updated successfully",
        "status": task.completed
    })


@router.post("/tasks")
async def load_tasks(
        db: db_session,
        tasks: List[TaskEntity]
):
    db.execute(text('DELETE FROM tasks'))
    db.commit()
    for task in tasks:
        result = db.query(Task).filter(Task.id == task.id).first()
        if result:
            db.execute(text('DELETE FROM tasks'))
            db.commit()
            raise HTTPException(
                status_code=422,
                detail="Task with id " + task.id + " already exists"
            )
        db_task = Task(
            id=task.id,
            text=task.text,
            completed=task.completed,
            created_at=task.created_at
        )
        db.add(db_task)
        db.commit()

    return JSONResponse({
        "message": "Tasks loaded successfully"
    })
