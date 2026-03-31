"""
Contribution router.
"""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db


router = APIRouter()


@router.get("/contributions", response_model=List[schemas.contribution.ContributionResponse])
def list_contributions(
    party_id: str | None = None,
    guest_id: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> List[schemas.contribution.ContributionResponse]:
    """
    List all contributions.
    """
    query = models.contribution.Contribution.query
    if party_id:
        query = query.filter(models.contribution.Contribution.party_id == party_id)
    if guest_id:
        query = query.filter(models.contribution.Contribution.guest_id == guest_id)
    contributions = query.limit(limit).offset(offset).all()
    return [
        schemas.contribution.ContributionResponse.model_validate(contribution)
        for contribution in contributions
    ]


@router.get("/contributions/{contribution_id}", response_model=schemas.contribution.ContributionResponse)
def get_contribution(
    contribution_id: str,
    db: Session = Depends(get_db),
) -> schemas.contribution.ContributionResponse:
    """
    Get a contribution by ID.
    """
    contribution = models.contribution.Contribution.query.get(contribution_id)
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contribution not found with ID: {contribution_id}",
        )
    return schemas.contribution.ContributionResponse.model_validate(contribution)


@router.post("/contributions", response_model=schemas.contribution.ContributionResponse, status_code=status.HTTP_201_CREATED)
def create_contribution(
    contribution: schemas.contribution.ContributionCreate,
    db: Session = Depends(get_db),
) -> schemas.contribution.ContributionResponse:
    """
    Create a new contribution.
    """
    new_contribution = models.contribution.Contribution(
        id=str(uuid.uuid4()),
        party_id=contribution.party_id,
        guest_id=contribution.guest_id,
        item_id=contribution.item_id,
        amount=contribution.amount,
        payment_ref=contribution.payment_ref,
        payment_status=contribution.payment_status,
        is_cash=contribution.is_cash,
        notes=contribution.notes,
    )

    db.add(new_contribution)
    db.commit()
    db.refresh(new_contribution)
    return schemas.contribution.ContributionResponse.model_validate(new_contribution)


@router.put("/contributions/{contribution_id}", response_model=schemas.contribution.ContributionResponse)
def update_contribution(
    contribution_id: str,
    contribution_update: schemas.contribution.ContributionUpdate,
    db: Session = Depends(get_db),
) -> schemas.contribution.ContributionResponse:
    """
    Update a contribution.
    """
    db_contribution = models.contribution.Contribution.query.get(contribution_id)
    if not db_contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contribution not found with ID: {contribution_id}",
        )

    for field, value in contribution_update.model_dump(exclude_unset=True).items():
        setattr(db_contribution, field, value)

    db.commit()
    db.refresh(db_contribution)
    return schemas.contribution.ContributionResponse.model_validate(db_contribution)


@router.delete("/contributions/{contribution_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contribution(
    contribution_id: str,
    db: Session = Depends(get_db),
) -> "fastapi.responses.JSONResponse":
    """
    Delete a contribution.
    """
    import fastapi

    contribution = models.contribution.Contribution.query.get(contribution_id)
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contribution not found with ID: {contribution_id}",
        )

    db.delete(contribution)
    db.commit()
    return fastapi.responses.JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
