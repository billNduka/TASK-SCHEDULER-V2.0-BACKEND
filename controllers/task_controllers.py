from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.models import Task
from schemas.task import TaskCreate, TaskUpdate
import datetime


# Get all tasks for a user
def get_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()


# Get a single task by ID
def get_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Create a new task
def create_task(db: Session, task: TaskCreate, user_id: int):
    new_task = Task(
        title=task.title,
        description=task.description,
        category=task.category,
        due_date=task.due_date,
        parent_id=task.parent_id,
        user_id=user_id
    )
    db.add(new_task) 
    db.commit()
    db.refresh(new_task)
    return new_task


# Update an existing task
def update_task(db: Session, task_id: int, task_data: TaskUpdate, user_id: int):
    task = get_task(db, task_id, user_id)

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    if task.completed and not task.completed_at:
        task.completed_at = datetime.datetime.utcnow()

    db.commit()
    db.refresh(task)
    return task


# Delete a task
def delete_task(db: Session, task_id: int, user_id: int):
    task = get_task(db, task_id, user_id)
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}
