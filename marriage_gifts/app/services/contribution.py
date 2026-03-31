"""
Contribution tracking service.
"""

import logging
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

from app.services.base import Service
from app.core.utils import generate_uuid
from app.core.exceptions import NotFoundException, ItemNotFundedException

logger = logging.getLogger(__name__)


class ContributionService(Service):
    """Service for managing contributions."""

    def __init__(self, repository=None):
        super().__init__(repository)

    async def make_contribution(
        self,
        party_id: str,
        guest_id: str,
        item_id: Optional[str] = None,
        amount: Decimal = Decimal("0"),
        is_cash: bool = False,
        notes: Optional[str] = None,
    ) -> dict:
        """Create a contribution record."""
        contribution_data = {
            "id": generate_contribution_id(),
            "party_id": party_id,
            "guest_id": guest_id,
            "item_id": item_id,
            "amount": amount,
            "payment_status": "pending",
            "payment_ref": None,
            "adjusted_from_item": None,
            "is_cash": is_cash,
            "notes": notes,
            "created_at": datetime.now(),
        }

        return contribution_data

    async def get_contribution(
        self,
        contribution_id: str,
    ) -> Optional[dict]:
        """Get contribution by ID."""
        return None

    async def get_party_contributions(
        self,
        party_id: str,
    ) -> List[dict]:
        """Get all contributions for a party."""
        return []

    async def update_contribution_status(
        self,
        contribution_id: str,
        payment_status: str,
        payment_ref: Optional[str] = None,
    ) -> dict:
        """Update contribution payment status."""
        return {"payment_status": payment_status}

    async def verify_and_complete_payment(
        self,
        contribution_id: str,
        payment_ref: str,
    ) -> dict:
        """Verify payment and complete contribution."""
        # In production: integrate with payment gateway API
        return {
            "contribution_id": contribution_id,
            "payment_status": "completed",
            "payment_ref": payment_ref,
        }

    def allocate_contribution_to_items(
        self,
        guest_id: str,
        party_id: str,
        amount: Decimal,
        items: List[dict],
        existing_contributions: List[dict],
    ) -> List[dict]:
        """
        Allocate guest's total contribution amount across items.

        This implements the overflow adjustment strategy:
        1. Calculate remaining capacity per item
        2. Sort items by remaining capacity (descending)
        3. Allocate contribution to items
        4. Handle overflow as cash contribution
        """
        from app.services.item import ItemService

        item_service = ItemService()
        allocations = item_service.calculate_item_contribution_allocation(
            guest_total_amount=amount,
            items=items,
            guest_contributions=existing_contributions,
        )

        return allocations

    def calculate_item_total_contributions(
        self,
        item: dict,
        contributions: List[dict],
    ) -> dict:
        """Calculate total contributions for an item."""
        total_contributed = sum(
            c.get("amount", Decimal(0))
            for c in contributions
            if c.get("item_id") == item.get("id")
        )

        return {
            "contributed_amount": total_contributed,
            "remaining": item.get("cost", Decimal(0)) - total_contributed,
            "funding_percentage": item_service.calculate_funding_percentage(
                total_contributed, item.get("cost", Decimal(0))
            ),
        }


def generate_contribution_id() -> str:
    """Generate a unique contribution ID."""
    return str(generate_uuid())
