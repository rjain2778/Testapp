"""
Party router.
"""

import uuid
from typing import List
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app import models, schemas
from app.database import get_db
from app.utils.parties import (
    calculate_party_duration,
    calculate_funding_for_guest,
    generate_unique_item_name,
)


router = APIRouter()


@router.get("/parties", response_model=List[schemas.party.PartyResponse])
def list_parties(
    limit: int = 100,
    offset: int = 0,
    active: bool | None = None,
    db: Session = Depends(get_db),
) -> List[schemas.party.PartyResponse]:
    """
    List all parties.
    """
    query = models.party.Party.query
    if active is not None:
        query = query.filter(models.party.Party.is_active == active)
    parties = query.limit(limit).offset(offset).all()
    return [
        schemas.party.PartyResponse.model_validate(party) for party in parties
    ]


@router.get("/parties/{party_id}", response_model=schemas.party.PartyResponse)
def get_party(
    party_id: str,
    db: Session = Depends(get_db),
) -> schemas.party.PartyResponse:
    """
    Get a party by ID.
    """
    party = models.party.Party.query.get(party_id)
    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party not found with ID: {party_id}",
        )
    return schemas.party.PartyResponse.model_validate(party)


@router.post("/parties", response_model=schemas.party.PartyResponse, status_code=status.HTTP_201_CREATED)
def create_party(
    party: schemas.party.PartyCreate,
    db: Session = Depends(get_db),
) -> schemas.party.PartyResponse:
    """
    Create a new party.
    """
    # Calculate duration
    duration = calculate_party_duration(
        start=party.start_date, end=party.end_date, currency=party.currency
    )

    # Create party instance
    new_party = models.party.Party(
        id=str(uuid.uuid4()),
        name=party.name,
        description=party.description,
        start_date=party.start_date,
        end_date=party.end_date,
        location=party.location,
        currency=party.currency,
        is_active=party.is_active if hasattr(party, "is_active") else True,
    )

    db.add(new_party)
    db.commit()
    db.refresh(new_party)
    return schemas.party.PartyResponse.model_validate(new_party)


@router.put("/parties/{party_id}", response_model=schemas.party.PartyResponse)
def update_party(
    party_id: str,
    party_update: schemas.party.PartyUpdate,
    db: Session = Depends(get_db),
) -> schemas.party.PartyResponse:
    """
    Update a party.
    """
    db_party = models.party.Party.query.get(party_id)
    if not db_party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party not found with ID: {party_id}",
        )

    for field, value in party_update.model_dump(exclude_unset=True).items():
        setattr(db_party, field, value)

    db.commit()
    db.refresh(db_party)
    return schemas.party.PartyResponse.model_validate(db_party)


@router.delete("/parties/{party_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_party(
    party_id: str,
    db: Session = Depends(get_db),
) -> JSONResponse:
    """
    Delete a party.
    """
    party = models.party.Party.query.get(party_id)
    if not party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party not found with ID: {party_id}",
        )

    db.delete(party)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
