from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.api.schemas.bank_account_schema import BankAccountSimpleResponseSchema
from app.api.schemas.transaction_type_schema import TransactionTypeSimpleResponseSchema
from app.api.schemas.payment_schema import PaymentResponseSchema


class BankTransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    description: str = Field(..., min_length=1)

    @field_validator("description", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class CreateDepositSchema(BankTransactionBase):
    bank_account_id: int


class BankTransactionResponseSchema(BankTransactionBase):
    id: int
    created_at: datetime

    bank_account: BankAccountSimpleResponseSchema
    transaction_type: TransactionTypeSimpleResponseSchema
    payment: Optional[PaymentResponseSchema] = None

    class Config:
        from_attributes = True
