"""
Party utility functions.
"""

from datetime import datetime
from decimal import Decimal


def calculate_party_duration(start: str, end: str, currency: str) -> int:
    """
    Calculate the duration of a party in days.

    Args:
        start: Start date in ISO format (YYYY-MM-DD)
        end: End date in ISO format (YYYY-MM-DD)
        currency: Currency code

    Returns:
        Duration in days
    """
    start_date = datetime.fromisoformat(start.replace("Z", ""))
    end_date = datetime.fromisoformat(end.replace("Z", ""))
    return (end_date - start_date).days


def calculate_funding_for_guest(contributions: list, total_cost: Decimal, is_cash: bool) -> Decimal:
    """
    Calculate the funding percentage for a guest's contributions.

    Args:
        contributions: List of contribution amounts
        total_cost: Total cost of the item
        is_cash: Whether this is a cash item

    Returns:
        Funding percentage as integer
    """
    if is_cash:
        return 0  # Cash items don't need funding percentage

    total_contributed = sum(c["amount"] for c in contributions if c["item_id"] is not None)
    if total_cost == 0:
        return 0
    return int((total_contributed / total_cost) * 100)


def generate_unique_item_name(base_name: str, party_id: str) -> str:
    """
    Generate a unique item name for a party.

    Args:
        base_name: Base name of the item
        party_id: Party ID to include in the name

    Returns:
        Unique item name
    """
    return f"{base_name} - {party_id[:8]}"
