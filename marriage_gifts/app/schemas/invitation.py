"""
Pydantic schemas for Invitation endpoints.
"""

from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict


class InvitationBase(BaseModel):
    """Invitation base schema."""

    party_id: str
    guest_id: str
    email: str
    name: str
    phone: Optional[str] = None


class InvitationCreate(InvitationBase):
    """Schema for creating an invitation."""

    passes_id: str = Field(..., max_length=32)
    expires_in_days: int = Field(default=30, ge=1, le=365)

    @property
    def invitation_token(self) -> str:
        return self.passes_id


class InvitationUpdate(BaseModel):
    """Schema for updating an invitation."""

    phone: Optional[str] = Field(None, max_length=20)
    declined_reason: Optional[str] = None


class InvitationResponse(InvitationBase):
    """Schema for invitation response."""

    id: str
    status: str
    invited_at: datetime
    expires_at: datetime
    accepted_at: Optional[datetime] = None
    declined_reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
