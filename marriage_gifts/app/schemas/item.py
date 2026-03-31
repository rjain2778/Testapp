"""
Pydantic schemas for Item endpoints.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ItemBase(BaseModel):
    """Item base schema."""

    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    image_url: Optional[str] = None
    platform: str = Field(..., max_length=50)
    product_url: str = Field(..., max_length=500)
    category: str = Field(..., max_length=100)
    cost: Decimal = Field(..., gt=0)
    is_cash: bool = Field(default=False)


class ItemCreate(ItemBase):
    """Schema for creating an item."""

    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item."""

    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    image_url: Optional[str] = None
    platform: Optional[str] = None
    product_url: Optional[str] = None
    category: Optional[str] = None
    cost: Optional[Decimal] = None


class ItemResponse(ItemBase):
    """Schema for item response."""

    id: str
    party_id: str
    cost: Decimal
    is_cash: bool
    status: str
    created_at: datetime
    updated_at: datetime
    contributed_amount: Decimal
    remaining: Decimal
    funding_percentage: int
    is_funded: bool

    model_config = ConfigDict(from_attributes=True)
