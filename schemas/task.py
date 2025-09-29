from enum import Enum
from pydantic import BaseModel
import datetime
from typing import Optional, List, Literal


class RecurrencePattern(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime.datetime] = None
    parent_id: Optional[int] = None
    category: str = "To-Do"
    scheduled_at: Optional[datetime.datetime] = None
    is_recurring: Optional[bool] = False
    recurrence_pattern: Optional[RecurrencePattern] = None
    quota: Optional[int] = None
    progress: Optional[int] = 0
    email_reminder: Optional[bool] = False


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

