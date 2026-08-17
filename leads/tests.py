from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from leads.models import Lead
from customers.models import Customer, Contact


class LeadWorkflowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='lead_rep',
            email='leadrep@test.com',
            password='password123',
            role=User.Role.SALES_REP
        )
        self.lead = Lead.objects.create(
            title='Cloud Upgrade Project',
            first_name='Alice',
            last_name='Smith',
            company='Stark Industries',
            email='alice@stark.com',
            phone='+1-555-0900',
            status=Lead.Status.QUALIFIED,
            assigned_to=self.user
        )

    def test_lead_conversion_workflow(self):
        client = Client()
        client.login(username='lead_rep', password='password123')

        # Trigger Lead Conversion POST
        response = client.post(reverse('lead-convert', kwargs={'pk': self.lead.pk}))
        self.assertEqual(response.status_code, 302)  # Redirects to Customer detail

        # Assert Lead updated to WON
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.status, Lead.Status.WON)

        # Assert Customer created
        customer = Customer.objects.get(email='alice@stark.com')
        self.assertEqual(customer.name, 'Stark Industries')

        # Assert Primary Contact created
        contact = Contact.objects.get(customer=customer)
        self.assertEqual(contact.first_name, 'Alice')
        self.assertTrue(contact.is_primary)
