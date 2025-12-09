from pydantic import BaseModel
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    description: str


class CreateRoleSchema(RoleBase):
    pass


class UpdateRoleSchema(RoleBase):
    pass


class RoleResponseSchema(RoleBase):
    id: int
    name: str
    description: str
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True
