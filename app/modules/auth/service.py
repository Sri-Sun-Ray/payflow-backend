from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.modules.auth.repository import AuthRepository
from app.modules.users.model import User


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repository = AuthRepository(db)

    async def register_user(
        self,
        full_name: str,
        email: str,
        password: str,
        phone: str | None = None,
    ) -> User:

        existing_user = await self.repository.get_user_by_email(email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
            phone=phone,
        )

        return await self.repository.create_user(user)

    async def login_user(
        self,
        email: str,
        password: str,
    ):

        user = await self.repository.get_user_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": "",
            "token_type": "bearer",
        }