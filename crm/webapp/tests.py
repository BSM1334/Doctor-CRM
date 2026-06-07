from django.test import TestCase
from django.urls import reverse

class PWATests(TestCase):
    def test_manifest_url(self):
        response = self.client.get(reverse('manifest'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        data = response.json()
        self.assertEqual(data['short_name'], 'Doctor CRM')

    def test_service_worker_url(self):
        response = self.client.get(reverse('service_worker'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/javascript')
        self.assertIn('CACHE_NAME', response.content.decode('utf-8'))
