"""
Item router.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.item import Item
from app.models.contribution import Contribution
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/", response_model=list[ItemResponse])
async def list_items(
    party_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all items for a party."""
    items = db.query(Item).filter(Item.party_id == party_id).order_by(
        Item.created_at.desc()
    )[skip:skip + limit].all()
    return items


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific item by ID."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item not found: {item_id}",
        )
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreate,
    db: Session = Depends(get_db),
):
    """Create a new item."""
    item = Item(
        id=item_data.id,
        party_id=item_data.party_id,
        name=item_data.name,
        description=item_data.description,
        image_url=item_data.image_url,
        platform=item_data.platform,
        product_url=item_data.product_url,
        category=item_data.category,
        cost=item_data.cost,
        is_cash=item_data.is_cash,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: str,
    item_data: ItemUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing item."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item not found: {item_id}",
        )

    update_data = item_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: str,
    db: Session = Depends(get_db),
):
    """Delete an item and its contributions."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item not found: {item_id}",
        )
    db.delete(item)
    db.commit()
    return None


@router.get("/{item_id}/funding")
async def get_item_funding(item_id: str, db: Session = Depends(get_db)):
    """Get detailed funding information for an item."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item not found: {item_id}",
        )

    contributions = db.query(Contribution).filter(
        Contribution.item_id == item_id,
    ).order_by(Contribution.created_at.desc()).all()

    return {
        "item": item.name,
        "total_cost": float(item.cost),
        "contributed_amount": float(item.contributed_amount),
        "remaining": float(item.remaining),
        "funding_percentage": item.funding_percentage,
        "contributors_count": item.contributors_count,
        "is_funded": item.is_funded,
        "contributions": [
            {
                "id": c.id,
                "guest_email": c.guest.email,
                "amount": float(c.amount),
                "is_cash": c.is_cash,
                "notes": c.notes,
                "payment_status": c.payment_status,
            }
            for c in contributions
        ],
    }
