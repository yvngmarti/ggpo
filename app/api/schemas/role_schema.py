from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    description: str


class CreateRoleSchema(RoleBase):
    pass


class UpdateRoleSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


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
