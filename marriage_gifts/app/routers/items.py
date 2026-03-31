"""
Item router.
"""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db


router = APIRouter()


@router.get("/items", response_model=List[schemas.item.ItemResponse])
def list_items(
    party_id: str | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> List[schemas.item.ItemResponse]:
    """
    List all items.
    """
    query = models.item.Item.query
    if party_id:
        query = query.filter(models.item.Item.party_id == party_id)
    if status:
        query = query.filter(models.item.Item.status == status)
    items = query.limit(limit).offset(offset).all()
    return [schemas.item.ItemResponse.model_validate(item) for item in items]


@router.get("/items/{item_id}", response_model=schemas.item.ItemResponse)
def get_item(
    item_id: str,
    db: Session = Depends(get_db),
) -> schemas.item.ItemResponse:
    """
    Get an item by ID.
    """
    item = models.item.Item.query.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item not found with ID: {item_id}",
        )
    return schemas.item.ItemResponse.model_validate(item)


@router.post("/items", response_model=schemas.item.ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item: schemas.item.ItemCreate,
    db: Session = Depends(get_db),
) -> schemas.item.ItemResponse:
    """
    Create a new item.
    """
    new_item = models.item.Item(
        id=str(uuid.uuid4()),
        party_id=item.party_id,
        name=item.name,
        description=item.description,
        image_url=item.image_url,
        platform=item.platform,
        product_url=item.product_url,
        category=item.category,
        cost=item.cost,
        is_cash=item.is_cash,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return schemas.item.ItemResponse.model_validate(new_item)


@router.put("/items/{item_id}", response_model=schemas.item.ItemResponse)
def update_item(
    item_id: str,
    item_update: schemas.item.ItemUpdate,
    db: Session = Depends(get_db),
) -> schemas.item.ItemResponse:
    """
    Update an item.
    """
    db_item = models.item.Item.query.get(item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item not found with ID: {item_id}",
        )

    for field, value in item_update.model_dump(exclude_unset=True).items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return schemas.item.ItemResponse.model_validate(db_item)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: str,
    db: Session = Depends(get_db),
) -> "fastapi.responses.JSONResponse":
    """
    Delete an item.
    """
    import fastapi

    item = models.item.Item.query.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item not found with ID: {item_id}",
        )

    db.delete(item)
    db.commit()
    return fastapi.responses.JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
