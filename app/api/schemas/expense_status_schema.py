from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class ExpenseStatusBase(BaseModel):
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class CreateExpenseStatusSchema(ExpenseStatusBase):
    pass


class UpdateExpenseStatusSchema(BaseModel):
    name: Optional[str] = None

    @field_validator("name", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class ExpenseStatusResponseSchema(ExpenseStatusBase):
    id: int
    name: str
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True
