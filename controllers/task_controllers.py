from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from dateutil.relativedelta import relativedelta
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
        due_date=task.due_date,
        parent_id=task.parent_id,
        category=task.category,
        scheduled_for=task.scheduled_for,
        is_recurring=task.is_recurring,
        recurrence_pattern=task.recurrence_pattern,
        quota=task.quota,
        progress=task.progress,
        email_reminder=task.email_reminder,
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

    if task.complete and task.completed:
        if task.recurrence_pattern == "daily":
            task.due_date += datetime.timedelta(days=1)
        elif task.recurrence_pattern == "weekly":
            task.due_date += datetime.timedelta(weeks=1)
        elif task.recurrence_pattern == "monthly":
            task.due_date += relativedelta(months=1)

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

# Update completion status
def update_completion_status(db: Session, task_id: int, user_id: int, amount: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.quota is None:
        raise HTTPException(status_code=400, detail="This task has no quota")

    task.progress += amount
    if task.progress >= task.quota:
        task.completed = True
        task.completed_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task

    

    

