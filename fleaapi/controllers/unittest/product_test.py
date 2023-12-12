from unittest.mock import MagicMock, patch

import pytest
from django.test import Client, TestCase
from django.urls import reverse

from fleaapi.models import Cart, Item, SellerProfile, User

from ..user import *


@pytest.mark.django_db
class ProductControllerTest(TestCase):
    def setUp(self):
        # Create test data for user and item
        self.user = User.objects.create(
            name="John Doe", email="jd@bu.edu", password="1234"
        )

        self.sellerProfile = SellerProfile.objects.create(
            user=self.user, phone="1234567890"
        )

        self.item = Item.objects.create(
            name="Test Item",
            location="Test Location",
            description="This is a description of the test item",
            seller_id=self.sellerProfile,  # Assuming seller_id is an instance of User
            category_id=None,  # Assuming category_id can be null
            price=100.0,
            image="path/to/image.jpg",
        )

    def test_get_item_info_by_id(self):
        # Assume you have a URL path 'get_item_info' to get item information
        url = f"/api/products/{str(self.item.id)}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)
        self.assertEqual(response.json()['name'], self.item.name)
        self.assertEqual(response.json()['description'], self.item.description)
        self.assertEqual(response.json()['price'], self.item.price)
        self.assertEqual(response.json()['image'], self.item.image)
        self.assertEqual(response.json()['location'], self.item.location)
        self.assertEqual(response.json()['seller_id'], self.item.seller_id.id)
        self.assertEqual(response.json()['category_id'], self.item.category_id)

        # More assertions can be added here to check other item information in the response

    def test_add_item_to_cart(self):
        # Assume you have a URL path 'add_item_to_cart' to add item to cart
        url = (
            "/api/add-item-to-cart/?user_id="
            + str(self.user.id)
            + "&product_id="
            + str(self.item.id)
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Cart.objects.filter(user_id=self.user.id, item_id=self.item.id).count(), 1
        )

        # More assertions can be added here to check if the item is added to the cart
