"""
Tests for party endpoints.
"""

from typing import Any
import httpx
import pytest
from fastapi.testclient import TestClient

from main import app


class TestPartyEndpoints:
    """Test cases for party endpoints."""

    def setup_method(self):
        """Setup test fixtures."""
        self.client = TestClient(app)
        self.base_url = "http://test" + app.url_path_for

    def test_create_party(self):
        """Test creating a new party."""
        data = {
            "name": "Test Wedding",
            "description": "Test Description",
            "start_date": "2024-05-01",
            "end_date": "2024-06-01",
            "location": "Test City",
        }
        response = self.client.post("/party/", json=data)
        assert response.status_code == 201
        party = response.json()
        assert party["name"] == "Test Wedding"

    def test_get_party(self):
        """Test getting a party by ID."""
        data = {
            "name": "Test Wedding",
            "start_date": "2024-05-01",
            "end_date": "2024-06-01",
            "location": "Test City",
        }
        response = self.client.post("/party/", json=data)
        party_id = response.json()["id"]

        response = self.client.get(f"/party/{party_id}/")
        assert response.status_code == 200

    def test_delete_party(self):
        """Test deleting a party."""
        data = {
            "name": "Test Wedding",
            "start_date": "2024-05-01",
            "end_date": "2024-06-01",
            "location": "Test City",
        }
        response = self.client.post("/party/", json=data)
        party_id = response.json()["id"]

        response = self.client.delete(f"/party/{party_id}/")
        assert response.status_code == 204
