"""
Tests for guest endpoints.
"""

from typing import Any
import httpx
import pytest
from fastapi.testclient import TestClient

from main import app


class TestGuestEndpoints:
    """Test cases for guest endpoints."""

    def setup_method(self):
        """Setup test fixtures."""
        self.client = TestClient(app)
        self.base_url = "http://test" + app.url_path_for

    def test_create_guest(self):
        """Test creating a new guest."""
        party_data = {
            "name": "Test Wedding",
            "start_date": "2024-05-01",
            "end_date": "2024-06-01",
            "location": "Test City",
        }
        self.client.post("/party/", json=party_data)
        party_id = response.json()["id"]

        data = {
            "party_id": party_id,
            "email": "test@example.com",
            "name": "Test Guest",
        }
        response = self.client.post("/guest/", json=data)
        assert response.status_code == 201

    def test_get_guest(self):
        """Test getting a guest by ID."""
        party_data = {
            "name": "Test Wedding",
            "start_date": "2024-05-01",
            "end_date": "2024-06-01",
            "location": "Test City",
        }
        response = self.client.post("/party/", json=party_data)
        party_id = response.json()["id"]

        guest_data = {
            "party_id": party_id,
            "email": "test@example.com",
            "name": "Test Guest",
        }
        response = self.client.post("/guest/", json=guest_data)
        guest_id = response.json()["id"]

        response = self.client.get(f"/guest/{guest_id}/")
        assert response.status_code == 200
