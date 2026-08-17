from django.test import TestCase, Client
from django.urls import reverse
from .models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='password123',
            role=User.Role.ADMIN
        )
        self.sales = User.objects.create_user(
            username='sales_test',
            email='sales@test.com',
            password='password123',
            role=User.Role.SALES_REP
        )

    def test_user_roles(self):
        self.assertTrue(self.admin.is_admin())
        self.assertTrue(self.admin.is_manager())
        self.assertFalse(self.sales.is_admin())
        self.assertTrue(self.sales.is_sales_rep())

    def test_login_view(self):
        client = Client()
        response = client.post(reverse('login'), {
            'username': 'admin_test',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after login
