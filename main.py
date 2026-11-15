from src.entities.dto.task.update import TaskUpdate
from src.entities.dto.task.create import TaskCreate
from psycopg.rows import dict_row
import psycopg
from fastapi import FastAPI


app = FastAPI()


DATABASE_URL: str = (
    "postgresql://postgres:12345@localhost:5432/fast_api"
)


@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int):
    return {"id": user_id}


@app.post("/tasks")
def create_task(task: TaskCreate):
    with psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    ) as conn:


        result = conn.execute(
        """
        INSERT INTO tasks
        (title, description, status, priority, due_date)
        VALUES
        (%s, %s, %s, %s, %s)
        RETURNING *
        """,
        (task.title, task.description, task.status, task.priority, task.due_date),
        )

        new_task = result.fetchone()

        return new_task

    
@app.get('/tasks')
def get_all_tasks():
    with psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    ) as conn:


        result = conn.execute(
        """
        SELECT * FROM tasks
        """,
        (),
        )

        tasks = result.fetchall()

        return tasks

@app.patch('/tasks/{task_id}')
def update_task_priority(task_id: int, body: TaskUpdate):
     with psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    ) as conn:

        result = conn.execute(
        """
        UPDATE tasks
        SET priority = %s
        WHERE id = %s
        RETURNING *
        """,
        (body.priority, task_id)
)


        updated_tasks = result.fetchone()

        return updated_tasks

@app.delete("/tasks/{task_id}")
def delete_task_by_id(task_id: int):
     with psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    ) as conn:
     
     
        result = conn.execute(
            """
            DELETE FROM tasks WHERE id = %s
            RETURNING id
            """,
        (task_id,)
        )

        deleted_task = result.fetchone()

        return deleted_task