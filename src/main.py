from fastapi import FastAPI

from src.routers import task as router_task


app = FastAPI()

app.include_router(router_task.router)

