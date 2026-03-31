"""
Pydantic schemas for Guest endpoints.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class GuestBase(BaseModel):
    """Guest base schema."""

    name: str = Field(..., max_length=200)
    email: str = Field(..., max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None


class GuestCreate(GuestBase):
    """Schema for creating a guest."""

    party_id: str


class GuestUpdate(BaseModel):
    """Schema for updating a guest."""

    name: Optional[str] = Field(None, max_length=200)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = None
    notes: Optional[str] = None
    accepted_at: Optional[datetime] = None
    declined_reason: Optional[str] = None


class GuestResponse(GuestBase):
    """Schema for guest response."""

    id: str
    party_id: str
    status: str
    notes: Optional[str] = None
    accepted_at: Optional[datetime] = None
    declined_reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
