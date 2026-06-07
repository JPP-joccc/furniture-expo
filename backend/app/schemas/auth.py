import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import Role


def _validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError("密码至少 8 位")
    if not re.search(r"[A-Za-z]", password):
        raise ValueError("密码需包含字母")
    if not re.search(r"\d", password):
        raise ValueError("密码需包含数字")
    return password


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1, max_length=100)
    role: Role
    shop_name: Optional[str] = Field(default=None, max_length=200)
    merchant_invite_code: Optional[str] = Field(default=None, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return _validate_password_strength(v)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: Role
    shop_name: Optional[str] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
