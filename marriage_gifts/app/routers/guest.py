"""
Guest router.
"""

import uuid
from typing import List
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app import models, schemas
from app.database import get_db


router = APIRouter()


@router.get("/guests", response_model=List[schemas.guest.GuestResponse])
def list_guests(
    party_id: str | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> List[schemas.guest.GuestResponse]:
    """
    List all guests.
    """
    query = models.guest.Guest.query
    if party_id:
        query = query.filter(models.guest.Guest.party_id == party_id)
    if status:
        query = query.filter(models.guest.Guest.status == status)
    guests = query.limit(limit).offset(offset).all()
    return [schemas.guest.GuestResponse.model_validate(guest) for guest in guests]


@router.get("/guests/{guest_id}", response_model=schemas.guest.GuestResponse)
def get_guest(
    guest_id: str,
    db: Session = Depends(get_db),
) -> schemas.guest.GuestResponse:
    """
    Get a guest by ID.
    """
    guest = models.guest.Guest.query.get(guest_id)
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guest not found with ID: {guest_id}",
        )
    return schemas.guest.GuestResponse.model_validate(guest)


@router.post("/guests", response_model=schemas.guest.GuestResponse, status_code=status.HTTP_201_CREATED)
def create_guest(
    guest: schemas.guest.GuestCreate,
    db: Session = Depends(get_db),
) -> schemas.guest.GuestResponse:
    """
    Create a new guest.
    """
    new_guest = models.guest.Guest(
        id=str(uuid.uuid4()),
        party_id=guest.party_id,
        name=guest.name,
        email=guest.email,
        phone=guest.phone,
        notes=guest.notes,
    )

    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)
    return schemas.guest.GuestResponse.model_validate(new_guest)


@router.put("/guests/{guest_id}", response_model=schemas.guest.GuestResponse)
def update_guest(
    guest_id: str,
    guest_update: schemas.guest.GuestUpdate,
    db: Session = Depends(get_db),
) -> schemas.guest.GuestResponse:
    """
    Update a guest.
    """
    db_guest = models.guest.Guest.query.get(guest_id)
    if not db_guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guest not found with ID: {guest_id}",
        )

    for field, value in guest_update.model_dump(exclude_unset=True).items():
        setattr(db_guest, field, value)

    db.commit()
    db.refresh(db_guest)
    return schemas.guest.GuestResponse.model_validate(db_guest)


@router.delete("/guests/{guest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guest(
    guest_id: str,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """
    Delete a guest.
    """
    guest = models.guest.Guest.query.get(guest_id)
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guest not found with ID: {guest_id}",
        )

    db.delete(guest)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
