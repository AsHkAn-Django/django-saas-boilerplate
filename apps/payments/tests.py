import json
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password123'
        )
        self.checkout_url = reverse('create-checkout-session')
        self.webhook_url = reverse('stripe-webhook')

    @patch('stripe.checkout.Session.create')
    def test_create_checkout_session_authenticated(self, mock_stripe_create):
        """
        Ensure an authenticated user can generate a Stripe Checkout URL.
        """
        # 1. Mock the Stripe response
        mock_stripe_create.return_value = MagicMock(url="https://checkout.stripe.com/test-url")

        # 2. Authenticate
        self.client.force_authenticate(user=self.user)

        # 3. Send Request (we don't need to send price_id, it should use the default)
        response = self.client.post(self.checkout_url)

        # 4. Check for 200 OK (If this fails with 500, check settings.FRONTEND_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['url'], "https://checkout.stripe.com/test-url")

        # 5. Verify we sent the correct user ID to Stripe
        mock_stripe_create.assert_called_once()
        self.assertEqual(
            mock_stripe_create.call_args[1]['client_reference_id'],
            self.user.id
        )

    @patch('stripe.Webhook.construct_event')
    def test_webhook_upgrades_user(self, mock_construct_event):
        """
        Ensure a valid webhook event upgrades the user to Pro.
        """
        # 1. Create a pure Python dictionary for the fake event
        # This is much safer than mocking __getitem__
        fake_event = {
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'client_reference_id': self.user.id,
                    'customer': 'cus_test123',
                    'subscription': 'sub_test123'
                }
            }
        }

        # 2. Tell the mock to return our simple dictionary
        mock_construct_event.return_value = fake_event

        # 3. Simulate the Webhook Request
        response = self.client.post(
            self.webhook_url,
            data=json.dumps(fake_event),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='fake_signature'
        )

        # 4. Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 5. Refresh user from DB to check updates
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_pro_member)
        self.assertEqual(self.user.stripe_customer_id, 'cus_test123')