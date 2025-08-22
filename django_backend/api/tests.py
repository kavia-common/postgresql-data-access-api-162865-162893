from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Record


class HealthTests(APITestCase):
    def test_health(self):
        url = reverse('Health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})


class RecordsAPITests(APITestCase):
    def setUp(self):
        # Seed test database with sample data
        Record.objects.create(name="alpha", value=1)
        Record.objects.create(name="beta", value=2)
        Record.objects.create(name="gamma", value=3)

    def test_list_records_returns_all_rows(self):
        url = reverse('RecordsList')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)
        names = [r['name'] for r in response.data]
        values = [r['value'] for r in response.data]
        self.assertListEqual(sorted(names), ["alpha", "beta", "gamma"])
        self.assertListEqual(sorted(values), [1, 2, 3])
