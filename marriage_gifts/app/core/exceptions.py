"""
Custom exceptions for the Marriage Gifts application.
"""

from typing import Optional
from pydantic import BaseModel
from fastapi import HTTPException


class AppException(Exception):
    """Base exception for the application."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class NotFoundException(AppException):
    """Exception raised when a resource is not found."""

    def __init__(self, resource: str, identifier: str):
        message = f"{resource} with id {identifier} not found"
        super().__init__(message, status_code=404)


class ValidationError(AppException):
    """Exception raised for validation errors."""

    def __init__(self, field: str, message: str):
        message = f"Validation error: {field} - {message}"
        super().__init__(message, status_code=422)


class PaymentFailedException(AppException):
    """Exception raised when payment fails."""

    def __init__(self, reference: str, error_message: str):
        message = f"Payment {reference} failed: {error_message}"
        super().__init__(message, status_code=500)


class InsufficientFundsException(AppException):
    """Exception raised when funds are insufficient."""

    def __init__(self, amount: float, required: float):
        message = f"Insufficient funds: available {amount}, required {required}"
        super().__init__(message, status_code=409)


class GuestNotInvitedException(AppException):
    """Exception raised when guest has not been invited."""

    def __init__(self, guest_email: str, party_id: str):
        message = f"Guest {guest_email} is not invited to party {party_id}"
        super().__init__(message, status_code=403)


class ItemNotAvailableException(AppException):
    """Exception raised when item is not available."""

    def __init__(self, item_id: str, reason: str):
        message = f"Item {item_id} not available: {reason}"
        super().__init__(message, status_code=400)


class ContributionLimitExceededException(AppException):
    """Exception raised when contribution limit is exceeded."""

    def __init__(self, contribution_id: str, limit: float, current: float):
        message = f"Contribution limit exceeded: {current}/{limit}"
        super().__init__(message, status_code=400)


class ItemNotFundedException(AppException):
    """Exception raised when item is not fully funded."""

    def __init__(self, item_id: str, item_name: str, current_amount: float, cost: float):
        message = (
            f"Item {item_name} not fully funded. "
            f"Contributed: {current_amount}, Cost: {cost}"
        )
        super().__init__(message, status_code=422)


# Custom HTTPException for FastAPI
def create_http_exception(
    status_code: int = 400,
    detail: str = "Error occurred",
    headers: Optional[dict] = None
) -> HTTPException:
    """Helper function to create HTTP exceptions."""
    return HTTPException(status_code=status_code, detail=detail, headers=headers)
