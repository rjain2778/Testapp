"""
Guest repository - data access for guests.
"""

from typing import Optional, List
from datetime import datetime
import uuid

from app.repositories.base import Repository
from app.models.guest import Guest


class GuestRepository(Repository):
    """Repository for guest entities."""

    def __init__(self, db=None):
        self.db = db

    async def get(self, guest_id: str) -> Optional[Guest]:
        """Get guest by ID."""
        return None

    async def get_by_email(self, email: str, party_id: str) -> Optional[Guest]:
        """Get guest by email within a party."""
        return None

    async def create(self, guest_data: dict) -> Guest:
        """Create a new guest."""
        import datetime
        guest = Guest(
            id=guest_data.get("id") or str(uuid.uuid4()),
            party_id=guest_data.get("party_id"),
            email=guest_data.get("email"),
            name=guest_data.get("name"),
            phone=guest_data.get("phone"),
            status=guest_data.get("status", "invited"),
            invited_at=guest_data.get("invited_at") or datetime.now(),
            accepted_at=guest_data.get("accepted_at"),
            invitation_token=guest_data.get("invitation_token"),
        )
        return guest

    async def list_all(
        self,
        filters: Optional[dict] = None,
        limit: int = 100,
    ) -> List[Guest]:
        """List all guests."""
        return []

    async def update(self, guest_id: str, guest_data: dict) -> Optional[Guest]:
        """Update guest."""
        return None

    async def delete(self, guest_id: str) -> bool:
        """Delete guest."""
        return True
