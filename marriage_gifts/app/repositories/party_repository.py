"""
Party repository - data access for gift parties.
"""

from typing import Optional, List
from datetime import datetime
import uuid

from app.repositories.base import Repository
from app.models.party import GiftParty


class PartyRepository(Repository):
    """Repository for gift party entities."""

    def __init__(self, db=None):
        self.db = db

    async def get(self, party_id: str) -> Optional[GiftParty]:
        """Get party by ID."""
        # In memory implementation
        return GiftParty(
            id=party_id,
            name="Demo Party",
            description="Demo Description",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30),
            location="Demo Location",
        )

    async def create(self, party_data: dict) -> GiftParty:
        """Create a new party."""
        import datetime
        party = GiftParty(
            id=party_data.get("id") or str(uuid.uuid4()),
            name=party_data.get("name"),
            description=party_data.get("description"),
            start_date=party_data.get("start_date"),
            end_date=party_data.get("end_date"),
            location=party_data.get("location"),
            currency=party_data.get("currency", "INR"),
            is_active=party_data.get("is_active", True),
            created_at=party_data.get("created_at") or datetime.now(),
            updated_at=party_data.get("updated_at") or datetime.now(),
        )
        return party

    async def list_all(
        self,
        filters: Optional[dict] = None,
        limit: int = 100,
    ) -> List[GiftParty]:
        """List all parties."""
        return []

    async def update(self, party_id: str, party_data: dict) -> Optional[GiftParty]:
        """Update party."""
        return None

    async def delete(self, party_id: str) -> bool:
        """Delete party."""
        return True


from datetime import timedelta
