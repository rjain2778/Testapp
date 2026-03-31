"""
Contribution SQLAlchemy model.
"""

from datetime import datetime
from decimal import Decimal
import uuid
import enum

from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class PAYMENT_STATUS(str, enum.Enum):
    """Payment status enumeration."""

    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"


class Contribution(Base):
    """Contribution model for tracking gift contributions."""

    __tablename__ = "contributions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    party_id = Column(String(36), ForeignKey("parties.id", ondelete="CASCADE"), nullable=False)
    guest_id = Column(String(36), ForeignKey("guests.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(String(36), ForeignKey("items.id", ondelete="SET NULL"), nullable=True)
    amount = Column(Decimal(10, 2), nullable=False, default=Decimal("0.00"))
    payment_status = Column(String(20), nullable=False, default="pending")
    payment_ref = Column(String(100), nullable=True)
    is_cash = Column(Boolean, default=False, nullable=False)
    notes = Column(String(500), nullable=True)

    adjusted_from_item_id = Column(String(36), nullable=True)

    created_at = Column(DateTime, default=func.now())

    # Relationships
    party = relationship("Party", back_populates="contributions")
    guest = relationship("Guest", back_populates="contributions")
    item = relationship("Item", back_populates="contributions")
