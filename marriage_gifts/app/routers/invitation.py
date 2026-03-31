"""
Invitation router.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.invitation import Invitation, INVITATION_STATUS
from app.models.guest import Guest
from app.schemas.invitation import InvitationCreate, InvitationResponse, InvitationUpdate

router = APIRouter(prefix="/invitations", tags=["Invitations"])


@router.get("/", response_model=list[InvitationResponse])
async def list_invitations(
    party_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all invitations for a party."""
    invitations = db.query(Invitation).filter(Invitation.party_id == party_id).order_by(
        Invitation.created_at.desc()
    )[skip:skip + limit].all()
    return invitations


@router.get("/{invitation_id}", response_model=InvitationResponse)
async def get_invitation(
    invitation_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific invitation by ID."""
    invitation = db.query(Invitation).filter(Invitation.id == invitation_id).first()
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation not found: {invitation_id}",
        )
    return invitation


@router.post("/", response_model=InvitationResponse, status_code=status.HTTP_201_CREATED)
async def create_invitation(
    invitation_data: InvitationCreate,
    db: Session = Depends(get_db),
):
    """Create a new invitation."""
    # Check if guest already has an active invitation
    existing = db.query(Invitation).filter(
        Invitation.guest_id == invitation_data.guest_id,
        Invitation.status.in_([INVITATION_STATUS.pending, INVITATION_STATUS.accepted]),
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Guest already has an active invitation",
        )

    # Check if guest exists
    guest = db.query(Guest).filter(Guest.id == invitation_data.guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guest not found: {invitation_data.guest_id}",
        )

    invitation = Invitation(
        id=invitation_data.id,
        party_id=invitation_data.party_id,
        guest_id=invitation_data.guest_id,
        email=invitation_data.email,
        name=invitation_data.name,
        phone=invitation_data.phone,
        invitation_token=invitation_data.invitation_token,
        invited_at=func.now(),
        expires_at=func.now() + func.interval(days=30),
    )
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return invitation


@router.delete("/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invitation(
    invitation_id: str,
    db: Session = Depends(get_db),
):
    """Delete an invitation."""
    invitation = db.query(Invitation).filter(Invitation.id == invitation_id).first()
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation not found: {invitation_id}",
        )
    db.delete(invitation)
    db.commit()
    return None


@router.get("/{invitation_id}/token")
async def get_invitation_token(invitation_id: str, db: Session = Depends(get_db)):
    """Get invitation token for email link."""
    invitation = db.query(Invitation).filter(Invitation.id == invitation_id).first()
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation not found: {invitation_id}",
        )

    return {
        "invitation_token": invitation.invitation_token,
        "party_id": invitation.party_id,
    }
