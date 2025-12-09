from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProviderBase(BaseModel):
    social_reason: str = Field(
        ..., min_length=1, description="Social reason minimum length must be 1"
    )
    rfc: str = Field(
        ...,
        min_length=12,
        max_length=13,
        description="RFC length must be 12 or 13",
    )
    address: str


class CreateProviderSchema(ProviderBase):
    pass


class UpdateProviderSchema(BaseModel):
    social_reason: Optional[str] = Field(None, min_length=1)
    rfc: Optional[str] = Field(None, min_length=12, max_length=13)
    address: Optional[str] = None


class ProviderResponseSchema(ProviderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
