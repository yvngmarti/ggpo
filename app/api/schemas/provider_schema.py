from pydantic import BaseModel, Field, field_validator
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

    @field_validator("social_reason", "rfc", "address", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class CreateProviderSchema(ProviderBase):
    pass


class UpdateProviderSchema(BaseModel):
    social_reason: Optional[str] = Field(None, min_length=1)
    rfc: Optional[str] = Field(None, min_length=12, max_length=13)
    address: Optional[str] = None

    @field_validator("social_reason", "rfc", "address", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class ProviderResponseSchema(ProviderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
