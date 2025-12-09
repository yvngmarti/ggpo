from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExpenseStatusBase(BaseModel):
    name: str


class CreateExpenseStatusSchema(ExpenseStatusBase):
    pass


class UpdateExpenseStatusSchema(BaseModel):
    name: Optional[str] = None


class ExpenseStatusResponseSchema(ExpenseStatusBase):
    id: int
    name: str
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True
