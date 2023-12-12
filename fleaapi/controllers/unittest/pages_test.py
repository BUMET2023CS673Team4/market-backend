from unittest.mock import MagicMock, patch

import pytest
from django.test import Client, TestCase

from fleaapi.models import SellerProfile, User

from ..pages import *


@pytest.mark.django_db
class PagesControllerTest(TestCase):
    def setUp(self) -> None:
        self.request = Client()
        self.all_categories = "/api/categories/"
        self.homepage = "/api/homepage/"
        self.category_items = "/api/categories/1/items/"

    def test_get_all_categories_empty(self):
        # remove all categories
        Category.objects.all().delete()
        response = self.request.get(self.all_categories)
        self.assertEqual(response.status_code, 200)

    def test_get_all_categories_one(self):
        # add one category
        Category.objects.create(name="test")
        response = self.request.get(self.all_categories)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["categories"]), 1)
        self.assertEqual(response.json()["categories"][0]["name"], "test")

    def test_get_all_categories_multiple(self):
        # add multiple categories
        Category.objects.create(name="test")
        Category.objects.create(name="test2")
        Category.objects.create(name="test3")
        response = self.request.get(self.all_categories)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["categories"]), 3)
        self.assertEqual(response.json()["categories"][0]["name"], "test")
        self.assertEqual(response.json()["categories"][1]["name"], "test2")
        self.assertEqual(response.json()["categories"][2]["name"], "test3")

    def test_get_homepage(self):
        # Setup
        u = User.objects.create(name="test", password="test")
        s = SellerProfile.objects.create(user=u)
        # add 3 categories
        c1 = Category.objects.create(name="testc")
        c2 = Category.objects.create(name="testc2")
        c3 = Category.objects.create(name="testc3")
        # add 3 items to each category
        Item.objects.create(
            name="test",
            description="test",
            price=1,
            category_id=c1,
            image="test.jpg",
            seller_id=s,
        )
        Item.objects.create(
            name="test2",
            description="test2",
            price=2,
            category_id=c1,
            image="test2.jpg",
            seller_id=s,
        )
        Item.objects.create(
            name="test3",
            description="test3",
            price=3,
            category_id=c1,
            image="test3.jpg",
            seller_id=s,
        )
        Item.objects.create(
            name="test4",
            description="test",
            price=1,
            category_id=c2,
            image="test4.jpg",
            seller_id=s,
        )
        Item.objects.create(
            name="test5",
            description="test2",
            price=2,
            category_id=c2,
            image="test5.jpg",
            seller_id=s,
        )
        Item.objects.create(
            name="test6",
            description="test3",
            price=3,
            category_id=c2,
            image="test6.jpg",
            seller_id=s,
        )
        Item.objects.create(
            name="test7",
            description="test",
            price=1,
            category_id=c3,
            image="test7.jpg",
            seller_id=s,
        )
        Item.objects.create(
            name="test8",
            description="test2",
            price=2,
            category_id=c3,
            image="test8.jpg",
            seller_id=s,
        )
        Item.objects.create(
            name="test9",
            description="test3",
            price=3,
            category_id=c3,
            image="test9.jpg",
            seller_id=s,
        )
        # Test
        response = self.request.get(self.homepage)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["name"], "testc")
        self.assertEqual(response.json()[0]["media_image"], "test.jpg")
        self.assertEqual(response.json()[1]["id"], 2)
        self.assertEqual(response.json()[1]["name"], "testc2")
        self.assertEqual(response.json()[1]["media_image"], "test4.jpg")
        self.assertEqual(response.json()[2]["id"], 3)
        self.assertEqual(response.json()[2]["name"], "testc3")
        self.assertEqual(response.json()[2]["media_image"], "test7.jpg")

    def test_get_category_items(self):
        # Setup
        u = User.objects.create(name="test", password="test")
        s = SellerProfile.objects.create(user=u)
        c1 = Category.objects.create(name="testc")
        Item.objects.create(
            name="test",
            description="test",
            price=1,
            category_id=c1,
            image="test.jpg",
            seller_id=s,
        )
        Item.objects.create(
            name="test2",
            description="test2",
            price=2,
            category_id=c1,
            image="test2.jpg",
            seller_id=s,
        )
        Item.objects.create(
            name="test3",
            description="test3",
            price=3,
            category_id=c1,
            image="test3.jpg",
            seller_id=s,
        )
        # Act
        response = self.request.get(self.category_items)

        # Assert
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(len(response_json["items"]), 3)
        self.assertEqual(response_json["items"][0]["id"], 1)
        self.assertEqual(response_json["items"][0]["name"], "test")
        self.assertEqual(response_json["items"][0]["price"], 1)
        self.assertEqual(response_json["items"][0]["media_image"], "test.jpg")
        self.assertEqual(response_json["items"][1]["id"], 2)
        self.assertEqual(response_json["items"][1]["name"], "test2")
        self.assertEqual(response_json["items"][1]["price"], 2)
        self.assertEqual(response_json["items"][1]["media_image"], "test2.jpg")
        self.assertEqual(response_json["items"][2]["id"], 3)
        self.assertEqual(response_json["items"][2]["name"], "test3")
        self.assertEqual(response_json["items"][2]["price"], 3)
        self.assertEqual(response_json["items"][2]["media_image"], "test3.jpg")
