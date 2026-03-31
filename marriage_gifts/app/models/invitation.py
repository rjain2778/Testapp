"""
Invitation SQLAlchemy model.
"""

from datetime import datetime
import uuid
import enum

from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class INVITATION_STATUS(str, enum.Enum):
    """Invitation status enumeration."""

    pending = "pending"
    accepted = "accepted"
    declined = "declined"
    expired = "expired"


class Invitation(Base):
    """Invitation model for sending invitations to guests."""

    __tablename__ = "invitations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    party_id = Column(String(36), ForeignKey("parties.id", ondelete="CASCADE"), nullable=False)
    guest_id = Column(String(36), ForeignKey("guests.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(255), nullable=False)
    name = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=True)
    invitation_token = Column(String(32), unique=True, nullable=False, default=lambda: str(uuid.uuid4())[:32])
    status = Column(String(20), default=INVITATION_STATUS.pending, nullable=False)
    invited_at = Column(DateTime, nullable=False, default=func.now())
    expires_at = Column(DateTime, nullable=False)
    accepted_at = Column(DateTime, nullable=True)
    declined_reason = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=func.now())

    # Relationships
    party = relationship("Party", back_populates="invitations")
    guest = relationship("Guest", back_populates="invitations")
