"""
Item SQLAlchemy model.
"""

from datetime import datetime
from decimal import Decimal
import uuid

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Item(Base):
    """Item model for gift registry items."""

    __tablename__ = "items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    party_id = Column(String(36), ForeignKey("parties.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    platform = Column(String(50), nullable=False)
    product_url = Column(String(500), nullable=False)
    category = Column(String(100), nullable=False)
    cost = Column(Decimal(10, 2), nullable=False, default=Decimal("0.00"))
    is_cash = Column(Boolean, default=False, nullable=False)

    # Computed fields (calculated after insert/update)
    status = Column(String(20), default="pending", nullable=False)
    contributed_amount = Column(Decimal(10, 2), default=Decimal("0.00"), nullable=False)
    remaining = Column(Decimal(10, 2), nullable=False)
    funding_percentage = Column(Integer, default=0, nullable=False)
    is_funded = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(
        DateTime,
        onupdate=func.now(),
        default=func.now(),
        nullable=False,
    )

    # Relationships
    party = relationship("Party", back_populates="items")
    contributions = relationship("Contribution", back_populates="item", lazy="dynamic")
    guest = relationship("Guest", back_populates="items_as_contributor", lazy="joined")
