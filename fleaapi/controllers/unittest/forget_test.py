from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class PasswordResetTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='old_password')
        self.client = Client()

    def test_request_password_reset(self):
        # Test successful password reset request
        response = self.client.post(reverse('request_password_reset'), {'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)  # Or the expected redirect status code

        # Test with non-existing user
        response = self.client.post(reverse('request_password_reset'), {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, 404)

    def test_reset_password(self):
        # Test successful password change
        response = self.client.post(reverse('reset_password'), {'email': 'test@example.com', 'new_password': 'new_password'})
        self.assertEqual(response.status_code, 200)

        # Verify password change
        self.assertTrue(self.user.check_password('new_password'))

        # Test with non-existing user
        response = self.client.post(reverse('reset_password'), {'email': 'nonexistent@example.com', 'new_password': 'new_password'})
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        # Clean up any objects if necessary
        pass