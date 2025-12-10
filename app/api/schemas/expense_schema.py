from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from app.api.schemas.expense_status_schema import ExpenseSimpleResponseSchema
from app.api.schemas.project_schema import ProjectSimpleResponseSchema
from app.api.schemas.provider_schema import ProviderSimpleResponseSchema
from app.api.schemas.user_schema import UserSimpleResponseSchema
from app.utils.constants import constants


class ExpenseBase(BaseModel):
    description: str = Field(..., min_length=1)
    total_amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    invoice_date: date
    evidence_url: Optional[str] = None

    @field_validator("description", "evidence_url", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class CreateExpenseSchema(ExpenseBase):
    project_id: int
    provider_id: int
    created_by_id: int


class UpdateExpenseSchema(BaseModel):
    description: Optional[str] = Field(None, min_length=1)
    total_amount: Optional[float] = Field(None, gt=0)
    invoice_date: Optional[date] = None
    evidence_url: Optional[str] = None
    project_id: Optional[int] = None
    provider_id: Optional[int] = None

    @field_validator("description", "evidence_url", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class ReviewExpenseSchema(BaseModel):
    reviewer_id: int
    action: str = Field(
        ...,
        pattern=f"^({constants.ACTION_APPROVE}|{constants.ACTION_REJECT})$",
        description="APPROVE or REJECT",
    )
    rejection_reason: Optional[str] = None

    @field_validator("rejection_reason", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class ExpenseResponseSchema(ExpenseBase):
    id: int
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    status: ExpenseSimpleResponseSchema
    project: ProjectSimpleResponseSchema
    provider: ProviderSimpleResponseSchema
    created_by: UserSimpleResponseSchema
    reviewed_by: Optional[UserSimpleResponseSchema] = None

    class Config:
        from_attributes = True
