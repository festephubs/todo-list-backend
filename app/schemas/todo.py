from datetime import datetime

from pydantic import BaseModel

from app.models.todo import TodoPriority, TodoStatus


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    priority: TodoPriority = TodoPriority.MEDIUM
    due_date: datetime | None = None


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TodoStatus | None = None
    priority: TodoPriority | None = None
    due_date: datetime | None = None


class TodoResponse(BaseModel):
    id: str
    title: str
    description: str | None
    status: TodoStatus
    priority: TodoPriority
    due_date: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    owner_id: str

    model_config = {"from_attributes": True}
