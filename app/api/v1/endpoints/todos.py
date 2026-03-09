from fastapi import APIRouter, Query

from app.api.deps import CurrentUser, DbSession
from app.models.todo import TodoStatus
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo import TodoService

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("", response_model=TodoResponse, status_code=201)
async def create_todo(data: TodoCreate, session: DbSession, current_user: CurrentUser):
    service = TodoService(session)
    return await service.create(data, owner_id=current_user.id)


@router.get("", response_model=list[TodoResponse])
async def list_todos(
    session: DbSession,
    current_user: CurrentUser,
    status: TodoStatus | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
):
    service = TodoService(session)
    return await service.get_all(current_user.id, status_filter=status, skip=skip, limit=limit)


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: str, session: DbSession, current_user: CurrentUser):
    service = TodoService(session)
    return await service.get_by_id(todo_id, owner_id=current_user.id)


@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str, data: TodoUpdate, session: DbSession, current_user: CurrentUser
):
    service = TodoService(session)
    return await service.update(todo_id, data, owner_id=current_user.id)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: str, session: DbSession, current_user: CurrentUser):
    service = TodoService(session)
    await service.delete(todo_id, owner_id=current_user.id)
