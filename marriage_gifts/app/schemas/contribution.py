"""
Pydantic schemas for Contribution endpoints.
"""

from decimal import Decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ContributionBase(BaseModel):
    """Contribution base schema."""

    amount: Decimal = Field(..., gt=0)
    is_cash: bool = Field(default=False)
    notes: Optional[str] = None


class ContributionCreate(ContributionBase):
    """Schema for creating a contribution."""

    party_id: str
    guest_id: str
    item_id: Optional[str] = None
    payment_ref: Optional[str] = None
    payment_status: Optional[str] = Field(default="pending")


class ContributionUpdate(BaseModel):
    """Schema for updating a contribution."""

    amount: Optional[Decimal] = None
    payment_status: Optional[str] = None
    payment_ref: Optional[str] = None
    is_cash: Optional[bool] = None
    notes: Optional[str] = None


class ContributionResponse(ContributionBase):
    """Schema for contribution response."""

    id: str
    party_id: str
    guest_id: str
    item_id: Optional[str] = None
    created_at: datetime
    adjusted_from_item_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
