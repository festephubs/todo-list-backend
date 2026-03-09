from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import CurrentUser, DbSession, enforce_login_cors, login_rate_limiter
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, session: DbSession):
    service = AuthService(session)
    return await service.register(data)


@router.post(
    "/login",
    response_model=Token,
    dependencies=[Depends(enforce_login_cors), Depends(login_rate_limiter)],
)
async def login(data: LoginRequest, session: DbSession):
    service = AuthService(session)
    try:
        return await service.login(data.username, data.password)
    except HTTPException as exc:
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sistema indisponível, tente mais tarde",
        ) from exc


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser):
    return current_user
