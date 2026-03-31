"""
Contribution repository - data access for contributions.
"""

from typing import Optional, List
from datetime import datetime
import uuid

from app.repositories.base import Repository
from app.models.contribution import Contribution


class ContributionRepository(Repository):
    """Repository for contribution entities."""

    def __init__(self, db=None):
        self.db = db

    async def get(self, contribution_id: str) -> Optional[Contribution]:
        """Get contribution by ID."""
        return None

    async def get_by_party(self, party_id: str) -> List[Contribution]:
        """Get all contributions for a party."""
        return []

    async def create(self, contribution_data: dict) -> Contribution:
        """Create a new contribution."""
        import datetime
        contribution = Contribution(
            id=contribution_data.get("id") or str(uuid.uuid4()),
            party_id=contribution_data.get("party_id"),
            guest_id=contribution_data.get("guest_id"),
            item_id=contribution_data.get("item_id"),
            amount=contribution_data.get("amount"),
            payment_status=contribution_data.get("payment_status", "pending"),
            payment_ref=contribution_data.get("payment_ref"),
            adjusted_from_item=contribution_data.get("adjusted_from_item"),
            is_cash=contribution_data.get("is_cash", False),
            notes=contribution_data.get("notes"),
            created_at=contribution_data.get("created_at") or datetime.now(),
        )
        return contribution

    async def update(self, contribution_id: str, contribution_data: dict) -> Optional[Contribution]:
        """Update contribution."""
        return None

    async def delete(self, contribution_id: str) -> bool:
        """Delete contribution."""
        return True
