"""
Contribution router.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.contribution import Contribution, PAYMENT_STATUS
from app.models.guest import Guest
from app.models.item import Item
from app.schemas.contribution import ContributionCreate, ContributionUpdate, ContributionResponse

router = APIRouter(prefix="/contributions", tags=["Contributions"])


@router.get("/", response_model=list[ContributionResponse])
async def list_contributions(
    party_id: str,
    item_id: str | None = None,
    guest_id: str | None = None,
    status: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all contributions for a party."""
    query = db.query(Contribution).filter(Contribution.party_id == party_id)

    if item_id:
        query = query.filter(Contribution.item_id == item_id)
    if guest_id:
        query = query.filter(Contribution.guest_id == guest_id)
    if status:
        query = query.filter(Contribution.payment_status == status)

    contributions = query.order_by(Contribution.created_at.desc())[skip:skip + limit].all()
    return contributions


@router.get("/{contribution_id}", response_model=ContributionResponse)
async def get_contribution(
    contribution_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific contribution by ID."""
    contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contribution not found: {contribution_id}",
        )
    return contribution


@router.post("/", response_model=ContributionResponse, status_code=status.HTTP_201_CREATED)
async def create_contribution(
    contribution_data: ContributionCreate,
    db: Session = Depends(get_db),
):
    """Create a new contribution."""
    # Validate guest exists
    guest = db.query(Guest).filter(Guest.id == contribution_data.guest_id).first()
    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Guest not found: {contribution_data.guest_id}",
        )

    # Check if contribution already exists
    existing = db.query(Contribution).filter(
        Contribution.party_id == contribution_data.party_id,
        Contribution.guest_id == contribution_data.guest_id,
        Contribution.item_id == contribution_data.item_id,
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contribution already exists",
        )

    contribution = Contribution(
        id=contribution_data.id,
        party_id=contribution_data.party_id,
        guest_id=contribution_data.guest_id,
        item_id=contribution_data.item_id,
        amount=contribution_data.amount,
        payment_status=contribution_data.payment_status or PAYMENT_STATUS.pending,
        payment_ref=contribution_data.payment_ref,
        is_cash=contribution_data.is_cash,
        notes=contribution_data.notes,
    )
    db.add(contribution)
    db.commit()
    db.refresh(contribution)

    # Update item's contributed amount
    if contribution.item_id:
        item = db.query(Item).filter(Item.id == contribution.item_id).first()
        if item:
            item.contributed_amount = item.contributed_amount + contribution.amount
            db.commit()

    return contribution


@router.patch("/{contribution_id}", response_model=ContributionResponse)
async def update_contribution(
    contribution_id: str,
    contribution_data: ContributionUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing contribution."""
    contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contribution not found: {contribution_id}",
        )

    update_data = contribution_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contribution, field, value)

    db.commit()
    db.refresh(contribution)
    return contribution


@router.post("/{contribution_id}/mark-completed", response_model=ContributionResponse)
async def mark_contribution_completed(
    contribution_id: str,
    db: Session = Depends(get_db),
):
    """Mark a contribution as completed."""
    contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contribution not found: {contribution_id}",
        )

    contribution.payment_status = PAYMENT_STATUS.completed
    db.commit()
    db.refresh(contribution)
    return contribution
