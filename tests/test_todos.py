import pytest
from httpx import AsyncClient


async def get_auth_header(client: AsyncClient) -> dict:
    await client.post(
        "/api/v1/auth/register",
        json={"name": "Todo User", "email": "todo@example.com", "password": "secret123"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "todo@example.com", "password": "secret123"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_todo(client: AsyncClient):
    headers = await get_auth_header(client)
    response = await client.post(
        "/api/v1/todos",
        json={"title": "My first todo", "priority": "high"},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My first todo"
    assert data["priority"] == "high"
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_list_todos(client: AsyncClient):
    headers = await get_auth_header(client)
    await client.post("/api/v1/todos", json={"title": "Todo 1"}, headers=headers)
    await client.post("/api/v1/todos", json={"title": "Todo 2"}, headers=headers)

    response = await client.get("/api/v1/todos", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_todo(client: AsyncClient):
    headers = await get_auth_header(client)
    create_resp = await client.post(
        "/api/v1/todos", json={"title": "Update me"}, headers=headers
    )
    todo_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/v1/todos/{todo_id}",
        json={"status": "completed"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["completed_at"] is not None


@pytest.mark.asyncio
async def test_delete_todo(client: AsyncClient):
    headers = await get_auth_header(client)
    create_resp = await client.post(
        "/api/v1/todos", json={"title": "Delete me"}, headers=headers
    )
    todo_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/todos/{todo_id}", headers=headers)
    assert response.status_code == 204

    response = await client.get(f"/api/v1/todos/{todo_id}", headers=headers)
    assert response.status_code == 404
