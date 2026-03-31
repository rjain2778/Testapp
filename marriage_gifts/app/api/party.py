"""
Party management API endpoints.
"""

from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal

from app.services.party import PartyService, generate_party_id
from app.api.deps import get_party_service, get_contribution_service, get_item_service
from app.config.api_settings import api_config

# Create router
router = APIRouter(prefix="/party", tags=["Parties"])


# Request/Response Models
class PartyCreate(BaseModel):
    """Party creation request."""
    name: str = Field(..., description="Gift party name")
    description: Optional[str] = Field(None, description="Optional description")
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: str = Field(..., description="End date in YYYY-MM-DD format")
    location: str = Field(..., description="Event location")
    currency: str = Field(default="INR", description="Currency code")


class PartyUpdate(BaseModel):
    """Party update request."""
    name: Optional[str] = Field(None, description="New party name")
    description: Optional[str] = Field(None, description="New description")
    location: Optional[str] = Field(None, description="New location")
    start_date: Optional[str] = Field(None, description="New start date")
    end_date: Optional[str] = Field(None, description="New end date")


class PartyResponse(BaseModel):
    """Party response model."""
    id: str
    name: str
    description: Optional[str]
    start_date: str
    end_date: str
    location: str
    currency: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class PartyListResponse(BaseModel):
    """List of parties response."""
    parties: List[PartyResponse]
    total: int


# Create party endpoint
@router.post("/", response_model=PartyResponse, status_code=status.HTTP_201_CREATED)
async def create_party(
    party_data: PartyCreate,
    party_service: PartyService = Depends(get_party_service),
):
    """
    Create a new gift party.

    - name: The name of the gift party
    - description: Optional description
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - location: Event location
    - currency: Currency code (default: INR)
    """
    try:
        party = await party_service.create_party(
            name=party_data.name,
            description=party_data.description,
            start_date=party_data.start_date,
            end_date=party_data.end_date,
            location=party_data.location,
            currency=party_data.currency,
        )

        return PartyResponse(**party)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Get party by ID
@router("/{party_id}", response_model=PartyResponse)
async def get_party(
    party_id: str,
    party_service: PartyService = Depends(get_party_service),
):
    """
    Get party by ID.

    - party_id: UUID of the party
    """
    party = await party_service.get_party(party_id=party_id)

    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party with id {party_id} not found",
        )

    return party


# Get party items
@router("/{party_id}/items", response_model=List[PartyResponse])
async def get_party_items(
    party_id: str,
    party_service: PartyService = Depends(get_party_service),
):
    """
    Get all items for a party.

    - party_id: UUID of the party
    """
    items = await party_service.get_party_items(party_id=party_id)

    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party with id {party_id} not found or no items",
        )

    return items


# Update party
@router("/{party_id}", response_model=PartyResponse)
async def update_party(
    party_id: str,
    party_data: PartyUpdate,
    party_service: PartyService = Depends(get_party_service),
):
    """
    Update party details.

    - party_id: UUID of the party
    - name: New party name (optional)
    - description: New description (optional)
    - location: New location (optional)
    - start_date: New start date (optional)
    - end_date: New end date (optional)
    """
    party = await party_service.update_party(
        party_id=party_id,
        name=party_data.name,
        description=party_data.description,
        location=party_data.location,
    )

    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party with id {party_id} not found",
        )

    return party


# Delete party
@router("/{party_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_party(
    party_id: str,
    party_service: PartyService = Depends(get_party_service),
):
    """
    Delete a party.

    - party_id: UUID of the party to delete
    """
    success = await party_service.delete_party(party_id=party_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party with id {party_id} not found",
        )

    # Return 204 No Content
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
