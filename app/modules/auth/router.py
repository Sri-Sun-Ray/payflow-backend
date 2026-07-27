from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from app.modules.auth.service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)

    return await service.register_user(
        full_name=request.full_name,
        email=request.email,
        password=request.password,
        phone=request.phone,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)

    return await service.login_user(
        email=request.email,
        password=request.password,
    )