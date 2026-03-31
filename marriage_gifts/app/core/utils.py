"""
Utility functions for the Marriage Gifts application.
"""

import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List, Dict, Any


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


def generate_invitation_token() -> str:
    """Generate a secure invitation token."""
    return uuid.uuid4().hex[:12]


def format_currency(amount: Decimal, currency: str = "INR") -> str:
    """Format amount as currency string."""
    symbol = {
        "INR": "₹",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
    }.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def calculate_funding_percentage(contributed: Decimal, total: Decimal) -> float:
    """Calculate funding percentage for an item."""
    if total == 0:
        return 0.0
    return round((contributed / total) * 100, 2)


def get_item_status(contributed: Decimal, total: Decimal) -> str:
    """Get item status based on funding."""
    if total == 0:
        return "pending"
    percentage = calculate_funding_percentage(contributed, total)
    if percentage >= 100:
        return "funded"
    elif percentage >= 50:
        return "partially_funded"
    return "pending"


def is_future_date(date_str: str) -> bool:
    """Check if date is in the future."""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.date() > datetime.now().date()
    except ValueError:
        return False


def date_range_between(start: str, end: str) -> bool:
    """Check if today's date is within start and end dates."""
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        today = datetime.now().date()
        return start_date <= today <= end_date
    except ValueError:
        return False


def truncate_string(text: str, max_length: int = 50) -> str:
    """Truncate string to maximum length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def capitalize_first_word(text: str) -> str:
    """Capitalize first word of text."""
    if not text:
        return text
    parts = text.split(maxsplit=1)
    if len(parts) == 1:
        return text.title()
    return parts[0].title() + " " + parts[1]


def generate_receipt_data(contribution: Dict[str, Any]) -> Dict[str, Any]:
    """Generate data for contribution receipt."""
    return {
        "receipt_id": generate_uuid(),
        "guest_name": contribution.get("guest_name", "N/A"),
        "party_name": contribution.get("party_name", "N/A"),
        "item_name": contribution.get("item_name", "N/A"),
        "item_platform": contribution.get("item_platform", "N/A"),
        "item_url": contribution.get("item_url", "N/A"),
        "amount": contribution.get("amount", Decimal(0)),
        "currency": contribution.get("currency", "INR"),
        "payment_ref": contribution.get("payment_ref", "N/A"),
        "is_cash": contribution.get("is_cash", False),
        "notes": contribution.get("notes", ""),
        "contribution_date": datetime.now().strftime("%Y-%m-%d"),
    }


def create_error_response(message: str, status_code: int = 400) -> Dict[str, Any]:
    """Create standardized error response."""
    return {
        "detail": message,
        "timestamp": datetime.now().isoformat(),
        "path": None,  # Will be set by FastAPI
    }


def create_success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Create standardized success response."""
    return {
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat(),
    }


def paginate_items(items: List[Any], page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """Paginate a list of items."""
    start = (page - 1) * page_size
    end = start + page_size
    paginated_items = items[start:end]

    return {
        "items": paginated_items,
        "page": page,
        "page_size": page_size,
        "total": len(items),
        "has_next": end < len(items),
        "has_prev": page > 1,
    }
