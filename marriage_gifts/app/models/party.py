"""
Party SQLAlchemy model.
"""

from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Party(Base):
    """Party model."""

    __tablename__ = "parties"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    currency = Column(String(3), default="INR", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(
        DateTime,
        onupdate=func.now(),
        default=func.now(),
        nullable=False,
    )

    # Relationships
    guests = relationship("Guest", back_populates="party", lazy="dynamic")
    items = relationship("Item", back_populates="party", lazy="dynamic")
    contributions = relationship("Contribution", back_populates="party", lazy="dynamic")
    invitations = relationship("Invitation", back_populates="party", lazy="dynamic")
