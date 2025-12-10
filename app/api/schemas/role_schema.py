from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    description: str

    @field_validator("name", "description", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class CreateRoleSchema(RoleBase):
    pass


class UpdateRoleSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    @field_validator("name", "description", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class RoleResponseSchema(RoleBase):
    id: int
    name: str
    description: str
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True


class RoleSimpleResponseSchema(RoleBase):
    class Config:
        from_attributes = True
