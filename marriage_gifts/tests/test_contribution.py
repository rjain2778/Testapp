"""
Tests for contribution endpoints.
"""

from typing import Any
import httpx
import pytest
from fastapi.testclient import TestClient

from main import app


class TestContributionEndpoints:
    """Test cases for contribution endpoints."""

    def setup_method(self):
        """Setup test fixtures."""
        self.client = TestClient(app)
        self.base_url = "http://test" + app.url_path_for

    def test_create_contribution(self):
        """Test creating a new contribution."""
        party_data = {
            "name": "Test Wedding",
            "start_date": "2024-05-01",
            "end_date": "2024-06-01",
            "location": "Test City",
        }
        party_response = self.client.post("/party/", json=party_data)
        party_id = party_response.json()["id"]

        item_data = {
            "party_id": party_id,
            "name": "Test Item",
            "product_url": "https://example.com",
            "cost": 100.0,
        }
        item_response = self.client.post("/item/", json=item_data)
        item_id = item_response.json()["id"]

        guest_data = {
            "party_id": party_id,
            "email": "test@example.com",
            "name": "Test Guest",
        }
        guest_response = self.client.post("/guest/", json=guest_data)
        guest_id = guest_response.json()["id"]

        contribution_data = {
            "party_id": party_id,
            "guest_id": guest_id,
            "amount": 50.0,
            "item_id": item_id,
        }
        response = self.client.post("/contribution/", json=contribution_data)
        assert response.status_code == 201

    def test_contribution_allocation(self):
        """Test contribution allocation to items."""
        party_data = {
            "name": "Test Wedding",
            "start_date": "2024-05-01",
            "end_date": "2024-06-01",
            "location": "Test City",
        }
        party_response = self.client.post("/party/", json=party_data)
        party_id = party_response.json()["id"]

        # Create items with different costs
        items_data = [
            {"name": "Item1", "product_url": "https://example.com", "cost": 100.0},
            {"name": "Item2", "product_url": "https://example.com", "cost": 100.0},
            {"name": "Item3", "product_url": "https://example.com", "cost": 100.0},
        ]
        for item_data in items_data:
            item_response = self.client.post("/item/", json={
                **item_data,
                "party_id": party_id,
            })
            assert item_response.status_code == 201

        # Create multiple guests
        guests_data = [
            {"email": f"test{i}@example.com", "name": f"Test Guest {i}"}
            for i in range(1, 4)
        ]
        for guest_data in guests_data:
            guest_response = self.client.post("/guest/", json={
                "party_id": party_id,
                **guest_data,
            })
            assert guest_response.status_code == 201

        # Create multiple contributions
        contributions_data = [
            {"guest_id": guest_id, "amount": 150.0, "item_id": None}
            for guest_id, guest in [
                (r["id"], r.json()) for r in [
                    self.client.post("/guest/", json={"party_id": party_id, **d})
                    for d in guests_data
                ]
            ]
        ]
        for contribution_data in contributions_data:
            contribution_response = self.client.post(
                "/contribution/", json={**contribution_data, "party_id": party_id}
            )
            assert contribution_response.status_code == 201

        # Verify overflow allocation
        item_responses = self.client.get(f"/item/{party_id}/")
        items = item_responses.json()["items"]
        # Items should have been partially funded, with some remaining

    def test_list_contributions(self):
        """Test listing contributions for a party."""
        party_data = {
            "name": "Test Wedding",
            "start_date": "2024-05-01",
            "end_date": "2024-06-01",
            "location": "Test City",
        }
        party_response = self.client.post("/party/", json=party_data)
        party_id = party_response.json()["id"]

        contribution_data = {
            "party_id": party_id,
            "guest_id": "test-guest-id",
            "amount": 50.0,
        }
        self.client.post("/contribution/", json=contribution_data)

        response = self.client.get(f"/contribution/{party_id}/")
        assert response.status_code == 200
