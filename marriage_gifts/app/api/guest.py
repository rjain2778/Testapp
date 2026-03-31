"""
Guest management API endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import uuid4

from app.services.guest import GuestService, generate_guest_id
from app.api.deps import get_guest_service, get_party_service
from app.config.api_settings import api_config

# Create router
router = APIRouter(prefix="/guest", tags=["Guests"])


# Request/Response Models
class GuestCreate(BaseModel):
    """Guest creation request."""
    party_id: str = Field(..., description="Party UUID")
    email: str = Field(..., description="Guest email")
    name: str = Field(..., description="Guest name")
    phone: Optional[str] = Field(None, description="Guest phone (optional)")


class GuestResponse(BaseModel):
    """Guest response model."""
    id: str
    party_id: str
    email: str
    name: str
    phone: Optional[str]
    status: str
    invited_at: datetime
    accepted_at: Optional[datetime]
    invitation_token: str


class GuestListResponse(BaseModel):
    """List of guests response."""
    guests: List[GuestResponse]
    total: int


# Create guest endpoint
@router.post("/", response_model=GuestResponse, status_code=status.HTTP_201_CREATED)
async def create_guest(
    guest_data: GuestCreate,
    guest_service: GuestService = Depends(get_guest_service),
    party_service: PartyService = Depends(get_party_service),
):
    """
    Create a new guest invitation.

    - party_id: UUID of the party
    - email: Guest email
    - name: Guest name
    - phone: Guest phone (optional)
    """
    # Validate party exists
    party = await party_service.get_party(party_id=guest_data.party_id)
    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party with id {guest_data.party_id} not found",
        )

    # Create guest
    guest = await guest_service.invite_guest(
        party_id=guest_data.party_id,
        email=guest_data.email,
        name=guest_data.name,
        phone=guest_data.phone,
    )

    return guest


# Get guest by ID
@router("/{guest_id}", response_model=GuestResponse)
async def get_guest(
    guest_id: str,
    guest_service: GuestService = Depends(get_guest_service),
):
    """
    Get guest by ID.

    - guest_id: UUID of the guest
    """
    guest = await guest_service.get_guest(guest_id=guest_id)

    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guest with id {guest_id} not found",
        )

    return guest


# Get guest by party and email
@router("/{party_id}/guest/{email}", response_model=GuestResponse)
async def get_guest_by_email(
    party_id: str,
    email: str,
    guest_service: GuestService = Depends(get_guest_service),
):
    """
    Get guest by party ID and email.

    - party_id: UUID of the party
    - email: Guest email
    """
    guest = await guest_service.get_guest_by_party(
        party_id=party_id,
        email=email,
    )

    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guest {email} for party {party_id} not found",
        )

    return guest


# List guests for a party
@router("/{party_id}", response_model=GuestListResponse)
async def list_guests(
    party_id: str,
    status: Optional[str] = None,
    guest_service: GuestService = Depends(get_guest_service),
):
    """
    List all guests for a party.

    - party_id: UUID of the party
    - status: Filter by status (optional)
    """
    guests = await guest_service.list_guests(
        party_id=party_id,
        status=status,
    )

    return GuestListResponse(
        guests=guests,
        total=len(guests),
    )
