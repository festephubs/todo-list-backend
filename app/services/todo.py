from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo, TodoStatus
from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate


class TodoService:
    def __init__(self, session: AsyncSession):
        self.repo = TodoRepository(session)

    async def create(self, data: TodoCreate, owner_id: str) -> TodoResponse:
        todo = Todo(
            title=data.title,
            description=data.description,
            priority=data.priority,
            due_date=data.due_date,
            owner_id=owner_id,
        )
        todo = await self.repo.create(todo)
        return TodoResponse.model_validate(todo)

    async def get_all(
        self,
        owner_id: str,
        status_filter: TodoStatus | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[TodoResponse]:
        todos = await self.repo.get_all(owner_id, status=status_filter, skip=skip, limit=limit)
        return [TodoResponse.model_validate(t) for t in todos]

    async def get_by_id(self, todo_id: str, owner_id: str) -> TodoResponse:
        todo = await self.repo.get_by_id(todo_id, owner_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found",
            )
        return TodoResponse.model_validate(todo)

    async def update(self, todo_id: str, data: TodoUpdate, owner_id: str) -> TodoResponse:
        todo = await self.repo.get_by_id(todo_id, owner_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found",
            )

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)

        if data.status == TodoStatus.COMPLETED and not todo.completed_at:
            todo.completed_at = datetime.now(UTC)
        elif data.status and data.status != TodoStatus.COMPLETED:
            todo.completed_at = None

        todo = await self.repo.update(todo)
        return TodoResponse.model_validate(todo)

    async def delete(self, todo_id: str, owner_id: str) -> None:
        todo = await self.repo.get_by_id(todo_id, owner_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found",
            )
        await self.repo.delete(todo)
