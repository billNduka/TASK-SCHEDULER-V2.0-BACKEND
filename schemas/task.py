from pydantic import BaseModel
import datetime
from typing import Optional, List

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime.datetime] = None
    parent_id: Optional[int] = None
    category: str = "To-Do"


class TaskCreate(TaskBase):
    pass  

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime.datetime] = None
    completed: Optional[bool] = None


class Task(TaskBase):
    id: int
    completed: bool
    created_at: datetime.datetime
    completed_at: Optional[datetime.datetime]
    user_id: int

    class Config:
        orm_mode = True

