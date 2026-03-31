"""
Invitation router.
"""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db


router = APIRouter()


@router.get("/invitations", response_model=List[schemas.invitation.InvitationResponse])
def list_invitations(
    party_id: str | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> List[schemas.invitation.InvitationResponse]:
    """
    List all invitations.
    """
    query = models.invitation.Invitation.query
    if party_id:
        query = query.filter(models.invitation.Invitation.party_id == party_id)
    if status:
        query = query.filter(models.invitation.Invitation.status == status)
    invitations = query.limit(limit).offset(offset).all()
    return [
        schemas.invitation.InvitationResponse.model_validate(invitation)
        for invitation in invitations
    ]


@router.get("/invitations/{invitation_id}", response_model=schemas.invitation.InvitationResponse)
def get_invitation(
    invitation_id: str,
    db: Session = Depends(get_db),
) -> schemas.invitation.InvitationResponse:
    """
    Get an invitation by ID.
    """
    invitation = models.invitation.Invitation.query.get(invitation_id)
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation not found with ID: {invitation_id}",
        )
    return schemas.invitation.InvitationResponse.model_validate(invitation)


@router.post("/invitations", response_model=schemas.invitation.InvitationResponse, status_code=status.HTTP_201_CREATED)
def create_invitation(
    invitation: schemas.invitation.InvitationCreate,
    db: Session = Depends(get_db),
) -> schemas.invitation.InvitationResponse:
    """
    Create a new invitation.
    """
    new_invitation = models.invitation.Invitation(
        id=invitation.id,
        party_id=invitation.party_id,
        guest_id=invitation.guest_id,
        email=invitation.email,
        name=invitation.name,
        phone=invitation.phone,
        invitation_token=invitation.invitation_token,
        status=invitation.status,
        invited_at=invitation.invited_at,
        expires_at=invitation.expires_at,
        accepted_at=invitation.accepted_at,
        declined_reason=invitation.declined_reason,
    )

    db.add(new_invitation)
    db.commit()
    db.refresh(new_invitation)
    return schemas.invitation.InvitationResponse.model_validate(new_invitation)


@router.put("/invitations/{invitation_id}", response_model=schemas.invitation.InvitationResponse)
def update_invitation(
    invitation_id: str,
    invitation_update: schemas.invitation.InvitationUpdate,
    db: Session = Depends(get_db),
) -> schemas.invitation.InvitationResponse:
    """
    Update an invitation.
    """
    db_invitation = models.invitation.Invitation.query.get(invitation_id)
    if not db_invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation not found with ID: {invitation_id}",
        )

    for field, value in invitation_update.model_dump(exclude_unset=True).items():
        setattr(db_invitation, field, value)

    db.commit()
    db.refresh(db_invitation)
    return schemas.invitation.InvitationResponse.model_validate(db_invitation)


@router.delete("/invitations/{invitation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invitation(
    invitation_id: str,
    db: Session = Depends(get_db),
) -> "fastapi.responses.JSONResponse":
    """
    Delete an invitation.
    """
    import fastapi

    invitation = models.invitation.Invitation.query.get(invitation_id)
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation not found with ID: {invitation_id}",
        )

    db.delete(invitation)
    db.commit()
    return fastapi.responses.JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
