from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from db import DB
from models import Category, Task

app = FastAPI()
db = DB("database.db")

class CategoryIn(BaseModel):
    name: str = Field(..., min_length=1)

class CategoryOut(CategoryIn):
    id: int


class TaskIn(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = ""
    done: Optional[bool] = False
    category_id: Optional[int] = None

class TaskOut(TaskIn):
    id: int

@app.get("/categories", response_model=List[CategoryOut])
def list_categories():
    return db.get_categories()


@app.post("/categories", response_model=CategoryOut)
def create_category(cat: CategoryIn):
    try:
        cid = db.add_category(cat.name)
        return {"id": cid, "name": cat.name}
    except Exception as e:
        raise HTTPException(400, str(e))


@app.put("/categories/{cid}", response_model=CategoryOut)
def update_category(cid: int, cat: CategoryIn):
    db.update_category(cid, cat.name)
    return {"id": cid, "name": cat.name}

@app.delete("/categories/{cid}")
def delete_category(cid: int):
    db.delete_category(cid)
    return {"status": "ok"}

@app.get("/tasks", response_model=List[TaskOut])
def list_tasks():
    return db.get_tasks()

@app.post("/tasks", response_model=TaskOut)
def create_task(t: TaskIn):
    tid = db.add_task(t.title, t.description, t.category_id)
    return {**t.dict(), "id": tid}

@app.get("/tasks/{tid}", response_model=TaskOut)
def get_task(tid: int):
    task = db.get_task(tid)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

@app.put("/tasks/{tid}", response_model=TaskOut)
def update_task(tid: int, t: TaskIn):
    db.update_task(tid, t.title, t.description, t.done, t.category_id)
    return db.get_task(tid)

@app.delete("/tasks/{tid}")
def delete_task(tid: int):
    db.delete_task(tid)
    return {"status": "ok"}

@app.on_event("shutdown")
def shutdown():
    db.close()