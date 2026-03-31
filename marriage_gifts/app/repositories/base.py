"""
Base repository class for common data access functionality.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Generic, TypeVar
from datetime import datetime

T = TypeVar('T')


class Repository(ABC, Generic[T]):
    """Base repository for data access abstraction."""

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        """Get a single record by ID."""
        pass

    @abstractmethod
    async def create(self, data: dict) -> T:
        """Create a new record."""
        pass

    @abstractmethod
    async def list_all(
        self,
        filters: Optional[dict] = None,
        limit: int = 100,
    ) -> List[T]:
        """List all records with optional filters."""
        pass

    @abstractmethod
    async def update(self, id: str, data: dict) -> Optional[T]:
        """Update a record by ID."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete a record by ID."""
        pass


class InMemoryRepository(Repository):
    """In-memory repository implementation for testing."""

    def __init__(self):
        self._storage = {}

    async def get(self, id: str) -> Optional[T]:
        """Get record by ID."""
        return self._storage.get(id)

    async def create(self, data: dict) -> T:
        """Create a new record."""
        record_id = data.get("id") or str(len(self._storage))
        self._storage[record_id] = data
        return data

    async def list_all(
        self,
        filters: Optional[dict] = None,
        limit: int = 100,
    ) -> List[T]:
        """List all records."""
        records = list(self._storage.values())
        if filters:
            for key, value in filters.items():
                records = [r for r in records if r.get(key) == value]
        return records[:limit]

    async def update(self, id: str, data: dict) -> Optional[T]:
        """Update a record."""
        if id in self._storage:
            self._storage[id].update(data)
            return self._storage[id]
        return None

    async def delete(self, id: str) -> bool:
        """Delete a record."""
        if id in self._storage:
            del self._storage[id]
            return True
        return False
