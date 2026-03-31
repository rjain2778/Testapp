"""
Item management API endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from decimal import Decimal

from app.services.item import ItemService, generate_item_id
from app.api.deps import get_item_service, get_party_service
from app.config.api_settings import api_config

# Create router
router = APIRouter(prefix="/item", tags=["Items"])


# Request/Response Models
class ItemCreate(BaseModel):
    """Item creation request."""
    party_id: str = Field(..., description="Party UUID")
    name: str = Field(..., description="Item name")
    description: Optional[str] = Field(None, description="Item description")
    image_url: Optional[str] = Field(None, description="Item image URL")
    platform: str = Field(default="amazon", description="E-commerce platform")
    product_url: str = Field(..., description="Product URL")
    category: str = Field(default="electronics", description="Item category")
    cost: Decimal = Field(..., description="Item cost")


class ItemUpdate(BaseModel):
    """Item update request."""
    name: Optional[str] = Field(None, description="New item name")
    description: Optional[str] = Field(None, description="New description")
    image_url: Optional[str] = Field(None, description="New image URL")
    platform: Optional[str] = Field(None, description="New platform")
    product_url: Optional[str] = Field(None, description="New product URL")


class ItemResponse(BaseModel):
    """Item response model."""
    id: str
    party_id: str
    name: str
    description: Optional[str]
    image_url: Optional[str]
    platform: str
    product_url: str
    category: str
    cost: Decimal
    contributed_amount: Decimal
    remaining: Decimal
    funding_percentage: float
    status: str
    created_at: datetime
    updated_at: datetime


class ItemListResponse(BaseModel):
    """List of items response."""
    items: List[ItemResponse]
    total: int


# Create item endpoint
@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreate,
    item_service: ItemService = Depends(get_item_service),
    party_service: PartyService = Depends(get_party_service),
):
    """
    Create a new item for a party.

    - party_id: UUID of the party
    - name: Item name
    - description: Item description (optional)
    - image_url: Item image URL (optional)
    - platform: E-commerce platform
    - product_url: Product URL
    - category: Item category
    - cost: Item cost
    """
    # Validate party exists
    party = await party_service.get_party(party_id=item_data.party_id)
    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party with id {item_data.party_id} not found",
        )

    # Create item
    item = await item_service.create_item(
        party_id=item_data.party_id,
        name=item_data.name,
        description=item_data.description,
        image_url=item_data.image_url,
        platform=item_data.platform,
        product_url=item_data.product_url,
        category=item_data.category,
        cost=item_data.cost,
    )

    return item


# Get item by ID
@router("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: str,
    item_service: ItemService = Depends(get_item_service),
):
    """
    Get item by ID.

    - item_id: UUID of the item
    """
    item = await item_service.get_item(item_id=item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )

    return item


# Get party items
@router("/{party_id}", response_model=ItemListResponse)
async def get_party_items(
    party_id: str,
    item_service: ItemService = Depends(get_item_service),
):
    """
    Get all items for a party.

    - party_id: UUID of the party
    """
    items = await item_service.get_party_items(party_id=party_id)

    return ItemListResponse(
        items=items,
        total=len(items),
    )


# Update item
@router("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: str,
    item_data: ItemUpdate,
    item_service: ItemService = Depends(get_item_service),
):
    """
    Update item details.

    - item_id: UUID of the item
    - name: New item name (optional)
    - description: New description (optional)
    - image_url: New image URL (optional)
    - platform: New platform (optional)
    - product_url: New product URL (optional)
    """
    item = await item_service.update_item(
        item_id=item_id,
        name=item_data.name,
        description=item_data.description,
        platform=item_data.platform,
        product_url=item_data.product_url,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )

    return item


# Delete item
@router("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: str,
    item_service: ItemService = Depends(get_item_service),
):
    """
    Delete an item.

    - item_id: UUID of the item to delete
    """
    success = await item_service.delete_item(item_id=item_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
