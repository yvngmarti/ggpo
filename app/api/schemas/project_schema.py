from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    name: str
    description: str
    code: str
    budget: float = Field(..., gt=0, description="Budget must be greater than 0")

    @field_validator("name", "description", "code", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class CreateProjectSchema(ProjectBase):
    pass


class UpdateProjectSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    budget: Optional[float] = Field(None, gt=0)

    @field_validator("name", "description", "code", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class ProjectResponseSchema(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectSimpleResponseSchema(ProjectBase):
    class Config:
        from_attributes = True
