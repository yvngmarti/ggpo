from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator


class TransactionTypeBase(BaseModel):
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class CreateTransactionTypeSchema(TransactionTypeBase):
    pass


class UpdateTransactionTypeSchema(BaseModel):
    name: Optional[str] = None

    @field_validator("name", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class TransactionTypeResponseSchema(TransactionTypeBase):
    id: int

    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True


class TransactionTypeSimpleResponseSchema(TransactionTypeBase):

    class Config:
        from_attributes = True
