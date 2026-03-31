"""
Pydantic schemas for Party endpoints.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class PartyBase(BaseModel):
    """Party base schema."""

    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    start_date: str  # ISO format date
    end_date: str  # ISO format date
    location: str = Field(..., max_length=255)
    currency: str = Field(default="INR", max_length=3)


class PartyCreate(PartyBase):
    """Schema for creating a party."""

    pass


class PartyUpdate(BaseModel):
    """Schema for updating a party."""

    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class PartyResponse(PartyBase):
    """Schema for party response."""

    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    duration_days: int

    model_config = ConfigDict(from_attributes=True)
