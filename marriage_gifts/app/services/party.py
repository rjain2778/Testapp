"""
Gift party management service.
"""

import logging
from typing import Optional
from decimal import Decimal
from datetime import datetime

from app.services.base import Service
from app.core.utils import (
    format_currency,
    calculate_funding_percentage,
    get_item_status,
)
from app.core.exceptions import (
    NotFoundException,
    ValidationException,
)

logger = logging.getLogger(__name__)


class PartyService(Service):
    """Service for managing gift parties."""

    def __init__(self, repository=None):
        super().__init__(repository)

    async def create_party(
        self,
        name: str,
        description: str,
        start_date: str,
        end_date: str,
        location: str,
        currency: str = "INR",
    ) -> dict:
        """Create a new gift party."""
        # Validate dates
        from datetime import datetime as dt
        start = dt.strptime(start_date, "%Y-%m-%d")
        end = dt.strptime(end_date, "%Y-%m-%d")

        if start >= end:
            raise ValueError("Start date must be before end date")

        party_data = {
            "id": generate_party_id(),
            "name": name,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
            "location": location,
            "currency": currency,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        return party_data

    async def get_party(self, party_id: str) -> Optional[dict]:
        """Get party by ID."""
        # In real implementation, fetch from repository
        return None

    async def update_party(
        self,
        party_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
    ) -> Optional[dict]:
        """Update party details."""
        # In real implementation, update in repository
        return None

    async def delete_party(self, party_id: str) -> bool:
        """Delete a party."""
        # In real implementation, delete from repository
        return True

    async def get_party_items(self, party_id: str) -> List[dict]:
        """Get all items for a party with funding status."""
        # In real implementation, fetch from repository
        return []

    def calculate_item_funding(
        self,
        item: dict,
        contributions: List[dict],
    ) -> dict:
        """Calculate item funding status from contributions."""
        contributed = sum(
            c.get("amount", Decimal(0)) for c in contributions
        )

        return {
            "contributed_amount": contributed,
            "remaining": item.get("cost", 0) - contributed,
            "funding_percentage": calculate_funding_percentage(
                contributed, item.get("cost", 0)
            ),
            "status": get_item_status(contributed, item.get("cost", 0)),
        }


def generate_party_id() -> str:
    """Generate a unique party ID."""
    import uuid
    return str(uuid.uuid4())
