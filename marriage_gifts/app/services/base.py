"""
Base service class for common functionality.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Any, TypeVar
from datetime import datetime


T = TypeVar('T')


class Service(ABC):
    """Base service class for business logic."""

    def __init__(self, repository: Optional[Any] = None):
        """Initialize service with repository dependency."""
        self.repository = repository

    @abstractmethod
    def perform_action(self) -> Any:
        """Perform the main service action."""
        pass

    def log_operation(self, operation: str, context: dict = None) -> None:
        """Log operation for debugging/auditing."""
        context = context or {}
        operation_log = {
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            **context
        }
        # In production, send to logging system
        print(operation_log)

    def validate_input(self, data: dict) -> dict:
        """Validate input data before processing."""
        # Implement in subclasses
        return data

    def handle_exception(self, exception: Exception) -> None:
        """Handle exceptions appropriately."""
        # Implement in subclasses
        raise exception
