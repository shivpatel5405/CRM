from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from customers.models import Customer


class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='api_user',
            email='api@test.com',
            password='password123',
            role=User.Role.SALES_REP
        )
        self.customer = Customer.objects.create(
            name='API Test Corp',
            email='api@corp.com'
        )

    def test_unauthenticated_api_access(self):
        response = self.client.get('/api/customers/')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_authenticated_api_access(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'API Test Corp')
