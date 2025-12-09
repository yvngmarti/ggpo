from pydantic import BaseModel, Field
from typing import Optional


class BankAccountBase(BaseModel):
    name: str
    account_number: str
    balance: float = Field(
        default=0.0, ge=0, description="Balance must be greater than or equal to 0"
    )


class CreateBankAccountSchema(BankAccountBase):
    pass


class UpdateBankAccountSchema(BaseModel):
    name: Optional[str] = None
    account_number: Optional[str] = None
    balance: Optional[float] = Field(None, ge=0)


class BankAccountResponseSchema(BankAccountBase):
    id: int

    class Config:
        from_attributes = True
