from collections import defaultdict
from time import monotonic
from typing import Annotated
from urllib.parse import urlparse

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import decode_access_token
from app.models.user import User
from app.services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

_MAX_LOGIN_ATTEMPTS = 5
_RATE_LIMIT_WINDOW_SECONDS = 60
_login_attempts: dict[str, list[float]] = defaultdict(list)

_ALLOWED_LOGIN_ORIGINS = {
    "http://localhost:4200",
    "http://127.0.0.1:4200",
}


def _get_client_key(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


async def login_rate_limiter(request: Request) -> None:
    client_key = _get_client_key(request)
    now = monotonic()

    recent_attempts = [
        timestamp
        for timestamp in _login_attempts[client_key]
        if now - timestamp < _RATE_LIMIT_WINDOW_SECONDS
    ]

    if len(recent_attempts) >= _MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )

    recent_attempts.append(now)
    _login_attempts[client_key] = recent_attempts


def _is_allowed_origin(origin: str, host: str | None) -> bool:
    if origin in _ALLOWED_LOGIN_ORIGINS:
        return True

    parsed_origin = urlparse(origin)
    if not parsed_origin.scheme or not parsed_origin.netloc:
        return False

    if host and parsed_origin.netloc == host:
        return True

    return False


async def enforce_login_cors(request: Request) -> None:
    origin = request.headers.get("origin")
    if not origin:
        return

    host = request.headers.get("host")
    if not _is_allowed_origin(origin, host):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Origin not allowed",
        )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    service = AuthService(session)
    return await service.get_current_user(user_id)


CurrentUser = Annotated[User, Depends(get_current_user)]
DbSession = Annotated[AsyncSession, Depends(get_session)]
