from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator


class PaymentStatusBase(BaseModel):
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class CreatePaymentStatusSchema(PaymentStatusBase):
    pass


class UpdatePaymentStatusSchema(BaseModel):
    name: Optional[str] = None

    @field_validator("name", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class PaymentStatusResponseSchema(PaymentStatusBase):
    id: int
    name: str
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        from_attributes = True


class PaymentStatusSimpleResponseSchema(PaymentStatusBase):
    class Config:
        from_attributes = True
