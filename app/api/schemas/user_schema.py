import re
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.api.schemas.role_schema import RoleSimpleResponseSchema


class UserBase(BaseModel):
    name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str

    @field_validator("name", "last_name", "email", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, v):
            raise ValueError("invalid email format")
        return v.lower()


class CreateUserSchema(UserBase):
    role_id: int
    password: str = Field(
        ..., min_length=12, description="Password must be at least 12 characters"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if not re.search(r"[A-Z]", v):
            raise ValueError("password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("password must contain at least one lower letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;~`]', v):
            raise ValueError("password must contain at least one special character")
        return v


class UpdateUserSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    email: Optional[str] = None
    role_id: Optional[int] = None
    password: Optional[str] = Field(None, min_length=12)

    @field_validator("name", "last_name", "email", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]):
        if v is None:
            return v
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, v):
            raise ValueError("invalid email format")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: Optional[str]):
        if v is None:
            return v
        if not re.search(r"[A-Z]", v):
            raise ValueError("password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("password must contain at least one lower letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;~`]', v):
            raise ValueError("password must contain at least one special character")

        return v


class UserResponseSchema(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    role: RoleSimpleResponseSchema

    class Config:
        from_attributes = True
