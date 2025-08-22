from django.urls import reverse
from django.utils.dateparse import parse_datetime
from rest_framework.test import APITestCase
from unittest.mock import patch

from .models import Record


class HealthTests(APITestCase):
    """Tests for the /api/health/ endpoint."""

    def test_health_ok_and_json(self):
        url = reverse("Health")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Validate content type comes from DRF JSON renderer
        self.assertIn("application/json", response["Content-Type"])
        # Validate exact payload
        self.assertEqual(response.data, {"message": "Server is up!"})


class RecordsAPITests(APITestCase):
    """Tests for the /api/records/ endpoint."""

    def setUp(self):
        # Seed test database with sample data
        self.r1 = Record.objects.create(name="alpha", value=1)
        self.r2 = Record.objects.create(name="beta", value=2)
        self.r3 = Record.objects.create(name="gamma", value=3)

    def test_list_records_returns_all_rows_and_fields(self):
        url = reverse("RecordsList")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

        # Ensure each element has expected keys and types
        required_keys = {"id", "name", "value", "created_at"}
        for item in response.data:
            self.assertEqual(set(item.keys()), required_keys)
            self.assertIsInstance(item["id"], int)
            self.assertIsInstance(item["name"], str)
            self.assertIsInstance(item["value"], int)
            # created_at should be ISO8601 string
            self.assertIsInstance(item["created_at"], str)
            self.assertIsNotNone(parse_datetime(item["created_at"]))

        names = [r["name"] for r in response.data]
        values = [r["value"] for r in response.data]
        self.assertListEqual(sorted(names), ["alpha", "beta", "gamma"])
        self.assertListEqual(sorted(values), [1, 2, 3])

    def test_list_records_sorted_by_id(self):
        """The view orders by id; verify stable ascending order."""
        url = reverse("RecordsList")
        resp = self.client.get(url)
        ids = [row["id"] for row in resp.data]
        self.assertEqual(ids, sorted(ids))

    def test_list_records_empty(self):
        """When there are no records, endpoint should return empty list."""
        Record.objects.all().delete()
        url = reverse("RecordsList")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_created_at_is_readonly_effectively(self):
        """Ensure created_at is present and not influenced by client input."""
        # Direct serializer write is not exposed by API; we check that the API output
        # always returns auto_now_add timestamps for created records.
        url = reverse("RecordsList")
        response = self.client.get(url)
        for item in response.data:
            # Ensure the created_at exists and appears as an ISO timestamp
            created_at = item["created_at"]
            parsed = parse_datetime(created_at)
            self.assertIsNotNone(parsed)

    def test_error_handling_returns_500_with_detail(self):
        """Simulate database error and ensure 500 with appropriate JSON detail."""
        url = reverse("RecordsList")
        with patch("api.views.Record.objects") as mock_manager:
            mock_manager.all.side_effect = Exception("db unavailable")
            response = self.client.get(url)
        self.assertEqual(response.status_code, 500)
        self.assertIn("detail", response.data)
        self.assertIn("Failed to retrieve records", response.data["detail"])
