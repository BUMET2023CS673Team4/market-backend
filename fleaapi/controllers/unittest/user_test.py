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
        self.assertEqual(response.status_code, 201)

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
