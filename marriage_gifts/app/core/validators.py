"""
Input validation functions for the Marriage Gifts application.
"""

from typing import Optional
from decimal import Decimal
import re


def validate_email(email: str) -> bool:
    """Validate email address format."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: Optional[str]) -> bool:
    """Validate phone number format (India)."""
    if not phone:
        return True
    # Format: +91XXXXXXXXXX or 98XXXXXXXXXX
    pattern = r'^(\+91|9[1-9]\d{2})(\d{4}(\d{4})?)?$'
    return bool(re.match(pattern, phone))


def validate_name(name: str) -> bool:
    """Validate name format (no special characters)."""
    if not name:
        return False
    return all(c.isalnum() or c in " -_" for c in name)


def validate_date(date_str: Optional[str]) -> bool:
    """Validate date format (YYYY-MM-DD)."""
    if not date_str:
        return True
    try:
        from datetime import datetime
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_datetime(datetime_str: Optional[str]) -> bool:
    """Validate datetime format (YYYY-MM-DDTHH:MM:SS)."""
    if not datetime_str:
        return True
    try:
        from datetime import datetime
        datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        return False


def validate_amount(amount: float) -> bool:
    """Validate amount is positive."""
    return amount > 0


def validate_cost(cost: float) -> bool:
    """Validate item cost is positive."""
    return cost > 0


def validate_url(url: str) -> bool:
    """Validate URL format."""
    if not url:
        return False
    # Simple URL validation
    return url.startswith("http://") or url.startswith("https://")


def validate_platform(platform: str) -> bool:
    """Validate e-commerce platform."""
    valid_platforms = ["amazon", "flipkart", "myntra", "furniture", "jewellery"]
    return platform.lower() in valid_platforms


def validate_category(category: str) -> bool:
    """Validate item category."""
    valid_categories = [
        "electronics", "furniture", "jewellery", "home",
        "clothing", "books", "appliances", "other"
    ]
    return category.lower() in valid_categories


def validate_guest_status(status: str) -> bool:
    """Validate guest status."""
    valid_statuses = ["invited", "attended", "declined", "pending"]
    return status.lower() in valid_statuses


def validate_item_status(status: str) -> bool:
    """Validate item status."""
    valid_statuses = ["pending", "partially_funded", "funded"]
    return status.lower() in valid_statuses


def validate_payment_status(status: str) -> bool:
    """Validate payment status."""
    valid_statuses = ["pending", "completed", "failed", "refunded"]
    return status.lower() in valid_statuses


# Batch validation function
def validate_contribution(data: dict) -> dict:
    """Validate contribution request data."""
    errors = []

    if not validate_amount(data.get("amount", 0)):
        errors.append("Amount must be greater than 0")

    item_id = data.get("item_id")
    if item_id:
        if not validate_platform(item_id):
            errors.append("Invalid item ID")

    if errors:
        raise ValueError("; ".join(errors))

    return data


def validate_party(data: dict) -> dict:
    """Validate party creation data."""
    errors = []

    if not validate_name(data.get("name", "")):
        errors.append("Name must be alphabetic characters only")

    if not validate_date(data.get("start_date")):
        errors.append("Start date must be in YYYY-MM-DD format")

    if not validate_date(data.get("end_date")):
        errors.append("End date must be in YYYY-MM-DD format")

    if errors:
        raise ValueError("; ".join(errors))

    return data


def validate_guest(data: dict) -> dict:
    """Validate guest creation data."""
    errors = []

    if not validate_email(data.get("email", "")):
        errors.append("Invalid email address")

    if "name" in data and not validate_name(data.get("name", "")):
        errors.append("Invalid name format")

    if "phone" in data and not validate_phone(data.get("phone")):
        errors.append("Invalid phone number format")

    if errors:
        raise ValueError("; ".join(errors))

    return data
