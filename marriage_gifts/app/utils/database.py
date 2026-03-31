"""
Database utilities.
"""

from sqlalchemy import text
from app.database import SessionLocal, engine


def init_db():
    """Initialize the database by creating all tables."""
    from app import models
    models.Base.metadata.create_all(bind=engine)
