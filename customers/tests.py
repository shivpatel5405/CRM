from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from customers.models import Customer, Contact


class CustomerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='rep',
            email='rep@test.com',
            password='password123',
            role=User.Role.SALES_REP
        )
        self.customer = Customer.objects.create(
            name='Test Acme Corp',
            email='contact@acmetest.com',
            company='Acme Corp',
            assigned_to=self.user
        )
        self.contact = Contact.objects.create(
            customer=self.customer,
            first_name='John',
            last_name='Doe',
            email='john@acmetest.com',
            is_primary=True
        )

    def test_customer_creation(self):
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(self.customer.contacts.count(), 1)
        self.assertEqual(str(self.customer), "Test Acme Corp (Acme Corp)")

    def test_customer_list_view_authenticated(self):
        client = Client()
        client.login(username='rep', password='password123')
        response = client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Acme Corp')
