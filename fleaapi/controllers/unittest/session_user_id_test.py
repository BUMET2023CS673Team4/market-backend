# this file is to test whether the user id is in the session
# if yes, return the user id and email
# if no, return error to frontend
import json
from django.test import Client, TestCase
from unittest.mock import MagicMock, patch

import pytest

from ..user import *
from fleaapi.models import User


@pytest.mark.django_db
class TestSessionUserId(TestCase):
    def setUp(self):
        self.client = Client()
        # create a user
        self.user = User.objects.create(
            name="John Doe", email="jd@bu.edu", password="123456"
        )
        self.user.save()

    def test_session_user_id(self):
        """
        Test whether the user id is in the session.
        if yes, return the user name and email
        if no, return error to frontend, show the frontend that the user is not logged in
        """

        # successful login and test whether the user id is in the session
        # login and get session
        response = self.client.post(
            "/api/login/",
            {"email": "jd@bu.edu", 'password': '123456'},
        )
        self.assertEqual(response.status_code, 302)
        # check whether the user id is in the session
        user_id = self.client.session.get('user_id')

        self.assertIsNotNone(user_id)
        self.assertEqual(user_id, self.user.id)
        #
        # if yes, return the user name and email
        response = self.client.get("/api/session/", {'user_id': user_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user_name'], 'John Doe')
        self.assertEqual(response.json()['user_email'], "jd@bu.edu")
