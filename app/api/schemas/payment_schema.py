from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field
from app.api.schemas.expense_schema import ExpenseResponseSchema
from app.api.schemas.payment_status_schema import PaymentStatusSimpleResponseSchema
from app.api.schemas.user_schema import UserSimpleResponseSchema
from app.utils.constants import constants


class PaymentBase(BaseModel):
    pass


class CreatePaymentSchema(PaymentBase):
    expense_id: int


class ProcessPaymentSchema(BaseModel):
    action: str = Field(
        ...,
        pattern=f"^({constants.PAYMENT_ACTION_PAY}|{constants.PAYMENT_ACTION_CANCEL})$",
        description="PAY or CANCEL",
    )
    bank_account_id: Optional[int] = None


class PaymentResponseSchema(PaymentBase):
    id: int
    amount: float
    payment_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    status: PaymentStatusSimpleResponseSchema
    expense: ExpenseResponseSchema
    created_by: UserSimpleResponseSchema
    processed_by: Optional[UserSimpleResponseSchema] = None

    class Config:
        from_attributes = True
