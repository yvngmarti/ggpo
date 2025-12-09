from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    description: str


class CreateRoleSchema(RoleBase):
    pass


class UpdateRoleSchema(RoleBase):
    pass
