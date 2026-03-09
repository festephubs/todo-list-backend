from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo, TodoStatus


class TodoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, todo: Todo) -> Todo:
        self.session.add(todo)
        await self.session.flush()
        return todo

    async def get_by_id(self, todo_id: str, owner_id: str) -> Todo | None:
        result = await self.session.execute(
            select(Todo).where(Todo.id == todo_id, Todo.owner_id == owner_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        owner_id: str,
        status: TodoStatus | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Todo]:
        query = select(Todo).where(Todo.owner_id == owner_id)
        if status:
            query = query.where(Todo.status == status)
        query = query.order_by(Todo.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, todo: Todo) -> Todo:
        await self.session.flush()
        return todo

    async def delete(self, todo: Todo) -> None:
        await self.session.delete(todo)
        await self.session.flush()
