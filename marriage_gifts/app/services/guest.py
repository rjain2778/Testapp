"""
Guest management service.
"""

import logging
from typing import Optional, List
from datetime import datetime

from app.services.base import Service
from app.core.utils import generate_invitation_token
from app.core.exceptions import NotFoundException

logger = logging.getLogger(__name__)


class GuestService(Service):
    """Service for managing guests and invitations."""

    def __init__(self, repository=None):
        super().__init__(repository)

    async def invite_guest(
        self,
        party_id: str,
        email: str,
        name: str,
        phone: Optional[str] = None,
    ) -> dict:
        """Create a guest invitation."""
        invitation_data = {
            "id": generate_guest_id(),
            "party_id": party_id,
            "email": email,
            "name": name,
            "phone": phone,
            "status": "invited",
            "invited_at": datetime.now(),
            "accepted_at": None,
            "invitation_token": generate_invitation_token(),
        }

        return invitation_data

    async def get_guest(self, guest_id: str) -> Optional[dict]:
        """Get guest by ID."""
        return None

    async def get_guest_by_party(
        self,
        party_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Optional[dict]:
        """Get guest by party and email/name."""
        return None

    async def list_guests(
        self,
        party_id: str,
        status: Optional[str] = None,
    ) -> List[dict]:
        """List all guests for a party."""
        return []

    async def revoke_invitation(self, guest_id: str) -> bool:
        """Revoke a guest invitation."""
        return True

    async def update_guest_status(
        self,
        guest_id: str,
        status: str,
        accepted_at: Optional[datetime] = None,
    ) -> dict:
        """Update guest status (attended/declined)."""
        return {"status": status}


def generate_guest_id() -> str:
    """Generate a unique guest ID."""
    import uuid
    return str(uuid.uuid4())
