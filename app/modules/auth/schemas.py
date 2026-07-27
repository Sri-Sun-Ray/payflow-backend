from pydantic import BaseModel, EmailStr, Field


from uuid import UUID


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    phone: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone: str | None
    is_active: bool
    is_verified: bool = False

    model_config = {
        "from_attributes": True
    }