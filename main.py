from fastapi import FastAPI

from src.api.routes import task as task_routes
from src.api.routes import user as user_routes

app = FastAPI(title="Todo API")

app.include_router(user_routes.router)
app.include_router(task_routes.router)


@app.get("/")
def root():
    return {"status": "ok"}