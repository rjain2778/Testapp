"""
Dependency injection for FastAPI endpoints.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from datetime import datetime, timedelta

# Import config
from app.config.api_settings import api_config

# JWT OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[dict]:
    """Dependency to get current authenticated user."""
    if not token:
        return None

    try:
        # Decode JWT token
        payload = jwt.decode(token, api_config.jwt_secret_key, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_or_create_repository(
    service_type: type,
    db_url: Optional[str] = None,
) -> object:
    """Get or create repository instance."""
    from app.repositories.base import InMemoryRepository

    # Return InMemoryRepository for development/testing
    return InMemoryRepository()


async def get_party_service() -> object:
    """Get party service instance."""
    from app.services.party import PartyService
    from app.repositories.party_repository import PartyRepository

    repo = PartyRepository()
    return PartyService(repo)


async def get_guest_service() -> object:
    """Get guest service instance."""
    from app.services.guest import GuestService
    from app.repositories.guest_repository import GuestRepository

    repo = GuestRepository()
    return GuestService(repo)


async def get_item_service() -> object:
    """Get item service instance."""
    from app.services.item import ItemService
    from app.repositories.item_repository import ItemRepository

    repo = ItemRepository()
    return ItemService(repo)


async def get_contribution_service() -> object:
    """Get contribution service instance."""
    from app.services.contribution import ContributionService
    from app.repositories.contribution_repository import ContributionRepository

    repo = ContributionRepository()
    return ContributionService(repo)


async def get_invitation_service() -> object:
    """Get invitation service instance."""
    from app.services.invitation import InvitationService
    from app.repositories.invitation_repository import InvitationRepository

    repo = InvitationRepository()
    return InvitationService(repo)


async def get_payment_service() -> object:
    """Get payment service instance."""
    from app.services.payment import payment_service
    return payment_service
