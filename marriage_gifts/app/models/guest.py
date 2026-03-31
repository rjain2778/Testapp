"""
Guest SQLAlchemy model.
"""

from datetime import datetime
import uuid
import enum

from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class GuestStatus(str, enum.Enum):
    """Guest status enumeration."""

    invited = "invited"
    accepted = "accepted"
    attended = "attended"
    declined = "declined"
    no_show = "no_show"
    cancelled = "cancelled"


class Guest(Base):
    """Guest model."""

    __tablename__ = "guests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    party_id = Column(String(36), ForeignKey("parties.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    status = Column(String(20), default="invited", nullable=False)
    notes = Column(String(500), nullable=True)
    accepted_at = Column(DateTime, nullable=True)
    declined_reason = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=func.now())

    # Relationships
    party = relationship("Party", back_populates="guests")
    invitations = relationship("Invitation", back_populates="guest", lazy="dynamic")
    contributions = relationship("Contribution", back_populates="guest", lazy="dynamic")
    items_as_contributor = relationship("Item", back_populates="guest")
