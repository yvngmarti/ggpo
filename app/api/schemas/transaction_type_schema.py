from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TransactionTypeBase(BaseModel):
    name: str


class CreateTransactionTypeSchema(TransactionTypeBase):
    pass


class UpdateTransactionTypeSchema(BaseModel):
    name: Optional[str] = None


class TransactionTypeResponseSchema(TransactionTypeBase):
    id: int
    name: str
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True
