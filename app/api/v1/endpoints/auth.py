from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, session: DbSession):
    service = AuthService(session)
    return await service.register(data)


@router.post("/login", response_model=Token)
async def login(data: UserLogin, session: DbSession):
    service = AuthService(session)
    return await service.login(data.email, data.password)


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser):
    return current_user
