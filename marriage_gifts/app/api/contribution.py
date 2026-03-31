"""
Contribution API endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from app.services.contribution import ContributionService, generate_contribution_id
from app.api.deps import get_contribution_service, get_guest_service, get_party_service, get_item_service
from app.config.api_settings import api_config

# Create router
router = APIRouter(prefix="/contribution", tags=["Contributions"])


# Request/Response Models
class ContributionCreate(BaseModel):
    """Contribution creation request."""
    party_id: str = Field(..., description="Party UUID")
    guest_id: str = Field(..., description="Guest UUID")
    amount: Decimal = Field(..., description="Contribution amount")
    item_id: Optional[str] = Field(None, description="Item UUID (optional)")
    notes: Optional[str] = Field(None, description="Notes (optional)")


class ContributionResponse(BaseModel):
    """Contribution response model."""
    id: str
    party_id: str
    guest_id: str
    item_id: Optional[str]
    amount: Decimal
    payment_status: str
    payment_ref: Optional[str]
    adjusted_from_item: Optional[str]
    is_cash: bool
    notes: Optional[str]
    created_at: datetime


class ContributionListResponse(BaseModel):
    """List of contributions response."""
    contributions: List[ContributionResponse]
    total: int


# Create contribution endpoint
@router.post("/", response_model=ContributionResponse, status_code=status.HTTP_201_CREATED)
async def create_contribution(
    contribution_data: ContributionCreate,
    contribution_service: ContributionService = Depends(get_contribution_service),
    guest_service: GuestService = Depends(get_guest_service),
    party_service: PartyService = Depends(get_party_service),
):
    """
    Create a new contribution.

    - party_id: UUID of the party
    - guest_id: UUID of the guest
    - amount: Contribution amount
    - item_id: Item UUID (optional - for specific item contribution)
    - notes: Notes (optional)
    """
    # Validate guest exists
    guest = await guest_service.get_guest(guest_id=contribution_data.guest_id)
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guest with id {contribution_data.guest_id} not found",
        )

    # Validate party exists
    party = await party_service.get_party(party_id=contribution_data.party_id)
    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party with id {contribution_data.party_id} not found",
        )

    # Create contribution
    contribution = await contribution_service.make_contribution(
        party_id=contribution_data.party_id,
        guest_id=contribution_data.guest_id,
        item_id=contribution_data.item_id,
        amount=contribution_data.amount,
        is_cash=contribution_data.is_cash,
        notes=contribution_data.notes,
    )

    return contribution


# Get contribution by ID
@router("/{contribution_id}", response_model=ContributionResponse)
async def get_contribution(
    contribution_id: str,
    contribution_service: ContributionService = Depends(get_contribution_service),
):
    """
    Get contribution by ID.

    - contribution_id: UUID of the contribution
    """
    contribution = await contribution_service.get_contribution(
        contribution_id=contribution_id,
    )

    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contribution with id {contribution_id} not found",
        )

    return contribution


# List contributions for a party
@router("/{party_id}", response_model=ContributionListResponse)
async def list_contributions(
    party_id: str,
    contribution_service: ContributionService = Depends(get_contribution_service),
):
    """
    List all contributions for a party.

    - party_id: UUID of the party
    """
    contributions = await contribution_service.get_party_contributions(
        party_id=party_id,
    )

    return ContributionListResponse(
        contributions=contributions,
        total=len(contributions),
    )


# Get all contributions for a guest
@router("/{party_id}/guest/{guest_id}", response_model=ContributionListResponse)
async def list_guest_contributions(
    party_id: str,
    guest_id: str,
    contribution_service: ContributionService = Depends(get_contribution_service),
):
    """
    List contributions made by a guest.

    - party_id: UUID of the party
    - guest_id: UUID of the guest
    """
    contributions = await contribution_service.get_party_contributions(
        party_id=party_id,
    )

    # Filter by guest
    guest_contributions = [
        c for c in contributions
        if c.get("guest_id") == guest_id
    ]

    return ContributionListResponse(
        contributions=guest_contributions,
        total=len(guest_contributions),
    )
