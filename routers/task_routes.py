from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.task import Task, TaskCreate, TaskUpdate
from controllers import task_controllers,auth_controllers
from models import models
from typing import List

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# GET all tasks
@router.get("/", response_model=List[Task])
def list_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(auth_controllers.get_current_user)):
    return task_controller.get_tasks(db, current_user.id)


# GET single task
@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth_controllers.get_current_user)):
    return task_controller.get_task(db, task_id, current_user.id)


# POST create task
@router.post("/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth_controllers.get_current_user)):
    return task_controller.create_task(db, task, current_user.id)


# PUT update task
@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth_controllers.get_current_user)):
    return task_controller.update_task(db, task_id, task_data, current_user.id)


# DELETE task
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth_controllers.get_current_user)):
    return task_controller.delete_task(db, task_id, current_user.id)


