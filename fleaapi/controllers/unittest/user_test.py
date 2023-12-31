from unittest.mock import MagicMock, patch

import pytest
from django.test import Client, TestCase

from ..user import *


@pytest.mark.django_db
class UserControllerTest(TestCase):
    def setUp(self) -> None:
        self.request = Client()
        self.api_path = "/api/signup/"

    def test_signup_with_valid_fields(self):
        response = self.request.post(
            self.api_path,
            {
                "name": "John Doe",
                "email": "jd@bu.edu",
                "password": "1234",
            },
        )
        self.assertRedirects(response, "/signin", fetch_redirect_response=False)

    def test_signup_with_missing_fields(self):
        response = self.request.post(self.api_path)
        self.assertEqual(response.status_code, 400)

    def test_signup_with_empty_fields(self):
        response = self.request.post(
            self.api_path,
            {
                "name": "",
                "email": "jd@bu.edu",
                "password": "",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_signup_with_invalid_email(self):
        response = self.request.post(
            self.api_path,
            {
                "name": "John Doe",
                "email": "jd@me@bu.edu",
                "password": "1234",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_signup_with_disallowed_email(self):
        response = self.request.post(
            self.api_path,
            {
                "name": "John Doe",
                "email": "jd@example.com",
                "password": "1234",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_signup_with_duplicated_emails(self):
        existing_user = User.objects.create(
            name="John Doe",
            email="jd@bu.edu",
            password="1234",
        )
        existing_user.save()
        response = self.request.post(
            self.api_path,
            {
                "name": "John Doe",
                "email": "jd@bu.edu",
                "password": "1234",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_signup_with_general_exception(self):
        with patch.object(User, User.save.__name__, side_effect=Exception("Boom!")):
            response = self.request.post(
                self.api_path,
                {
                    "name": "John Doe",
                    "email": "jd@bu.edu",
                    "password": "1234",
                },
            )
            self.assertEqual(response.status_code, 500)

    def test_login_with_valid_credentials(self):
        existing_user = User.objects.create(
            name="John Doe", email="jd@bu.edu", password="1234"
        )
        response = self.client.post(
            "/api/login/",
            data={
                "email": "jd@bu.edu",
                "password": "1234",
            },
        )
        self.assertRedirects(response, "/", fetch_redirect_response=False)

    def test_login_with_invalid_credentials(self):
        existing_user = User.objects.create(
            name="John Doe", email="jd@bu.edu", password="1234"
        )
        response = self.client.post(
            "/api/login/",
            data={
                "email": "jd@bu.edu",
                "password": "12345",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_login_with_invalid2_credentials(self):
        existing_user = User.objects.create(
            name="John Doe", email="jd@bu.edu", password="1234"
        )
        response = self.client.post(
            "/api/login/",
            data={
                "email": "jd@u.edu",
                "password": "1234",
            },
        )
        self.assertEqual(response.status_code, 400)
