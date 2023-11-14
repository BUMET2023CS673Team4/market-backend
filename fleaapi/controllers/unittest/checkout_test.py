from unittest.mock import MagicMock, patch

import pytest
from django.test import Client, TestCase

from ..checkout import *


class CheckoutControllerTest(TestCase):
    def setUp(self) -> None:
        self.request = Client()
        self.stripe_public_key = "/api/stripe-public-key/"
        self.create_checkout_session = "/api/create-checkout-session/"
        self.session_status = "/api/session-status/"

    def test_get_stripe_public_key(self):
        with patch.object(
            SecretProvider, SecretProvider.get_secret.__name__, return_value="test_key"
        ):
            response = self.request.get(self.stripe_public_key)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['public_key'], "test_key")

    def test_create_checkout_session(self):
        with (
            patch.object(
                SecretProvider,
                SecretProvider.get_secret.__name__,
                return_value="test_key",
            ),
            patch.object(
                stripe.Product, stripe.Product.create.__name__, return_value=MagicMock()
            ),
            patch.object(
                stripe.Price, stripe.Price.create.__name__, return_value=MagicMock()
            ),
            patch.object(
                stripe.checkout.Session,
                stripe.checkout.Session.create.__name__,
                return_value=MagicMock(client_secret="test_session_id"),
            ),
        ):
            response = self.request.post(self.create_checkout_session)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['client_secret'], "test_session_id")

    def test_create_checkout_session_exception(self):
        with (
            patch.object(
                SecretProvider,
                SecretProvider.get_secret.__name__,
                return_value="test_key",
            ),
            patch.object(
                stripe.Product, stripe.Product.create.__name__, return_value=MagicMock()
            ),
            patch.object(
                stripe.Price, stripe.Price.create.__name__, return_value=MagicMock()
            ),
            patch.object(
                stripe.checkout.Session,
                stripe.checkout.Session.create.__name__,
                side_effect=Exception("test_exception"),
            ),
        ):
            response = self.request.post(self.create_checkout_session)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json()['error'], "test_exception")

    def test_session_status(self):
        with patch.object(
            stripe.checkout.Session,
            stripe.checkout.Session.retrieve.__name__,
            return_value=MagicMock(
                status="paid", customer_details=MagicMock(email="test@test.com")
            ),
        ):
            response = self.request.get(self.session_status + "?stripe_sid=test_sid")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['status'], "paid")
            self.assertEqual(response.json()['customer_email'], "test@test.com")

    def test_session_status_exception(self):
        with patch.object(
            stripe.checkout.Session,
            stripe.checkout.Session.retrieve.__name__,
            side_effect=Exception("test_exception"),
        ):
            response = self.request.get(self.session_status + "?stripe_sid=test_sid")
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json()['error'], "test_exception")

    def test_session_status_missing_sid(self):
        response = self.request.get(self.session_status)
        self.assertEqual(response.status_code, 500)
