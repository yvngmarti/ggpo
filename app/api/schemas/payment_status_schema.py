from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentStatusBase(BaseModel):
    name: str


class CreatePaymentStatusSchema(PaymentStatusBase):
    pass


class UpdatePaymentStatusSchema(BaseModel):
    name: Optional[str] = None


class PaymentStatusResponseSchema(PaymentStatusBase):
    id: int
    name: str
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True
