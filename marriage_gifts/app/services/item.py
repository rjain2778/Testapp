"""
Item/wishlist management service.
"""

import logging
from typing import Optional, List
from decimal import Decimal

from app.services.base import Service
from app.core.utils import (
    get_item_status,
    calculate_funding_percentage,
)

logger = logging.getLogger(__name__)


class ItemService(Service):
    """Service for managing gift items/wishlist."""

    def __init__(self, repository=None):
        super().__init__(repository)

    async def create_item(
        self,
        party_id: str,
        name: str,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
        platform: str = "amazon",
        product_url: str = "",
        category: str = "electronics",
        cost: Decimal = Decimal("0"),
    ) -> dict:
        """Create a new item for a party."""
        item_data = {
            "id": generate_item_id(),
            "party_id": party_id,
            "name": name,
            "description": description,
            "image_url": image_url,
            "platform": platform,
            "product_url": product_url,
            "category": category,
            "cost": cost,
            "contributed_amount": Decimal("0"),
            "status": "pending",
        }

        return item_data

    async def get_item(self, item_id: str) -> Optional[dict]:
        """Get item by ID."""
        return None

    async def get_party_items(self, party_id: str) -> List[dict]:
        """Get all items for a party."""
        return []

    async def delete_item(self, item_id: str) -> bool:
        """Delete an item."""
        return True

    async def update_item(
        self,
        item_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        platform: Optional[str] = None,
        product_url: Optional[str] = None,
    ) -> dict:
        """Update item details."""
        return None

    def calculate_item_contribution_allocation(
        self,
        guest_total_amount: Decimal,
        items: List[dict],
        existing_contributions: List[dict],
    ) -> List[dict]:
        """
        Allocate guest's contribution to items.

        Strategy:
        1. Calculate remaining capacity per item
        2. Sort items by remaining capacity (descending)
        3. Allocate contribution to items
        4. Handle overflow (cash contribution)
        """
        # Calculate remaining capacity per item
        for item in items:
            item_remaining = item.get("cost", Decimal(0)) - item.get(
                "contributed_amount", Decimal(0)
            )
            item["remaining"] = item_remaining

        # Sort items by remaining capacity (descending)
        items_by_remaining = sorted(
            items, key=lambda x: x.get("remaining", Decimal(0)), reverse=True
        )

        # Allocate contribution to items
        allocations = []
        total_allocated = Decimal("0")

        for item in items_by_remaining:
            available = item.get("remaining", Decimal(0)) - sum(
                c.get("amount", Decimal(0))
                for c in existing_contributions
                if c.get("item_id") == item.get("id")
            )

            if available > 0:
                allocate = min(
                    available,
                    guest_total_amount - total_allocated,
                )
                # Create allocation record
                allocations.append({
                    "item_id": item.get("id"),
                    "amount": allocate,
                    "is_cash": False,
                })
                total_allocated += allocate

        # Check for overflow (cash contribution)
        remaining_after_items = guest_total_amount - total_allocated
        if remaining_after_items > 0:
            allocations.append({
                "item_id": None,
                "amount": remaining_after_items,
                "is_cash": True,
            })

        return allocations


def generate_item_id() -> str:
    """Generate a unique item ID."""
    import uuid
    return str(uuid.uuid4())
