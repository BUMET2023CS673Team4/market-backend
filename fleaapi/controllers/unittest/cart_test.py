from unittest.mock import MagicMock, patch

import pytest
from django.contrib.sessions.backends import db
from django.test import Client, TestCase

from fleaapi.models import Cart, Item, SellerProfile, User


@pytest.mark.django_db
class CartControllerTest(TestCase):
    def setUp(self):
        # Create test data for user and item
        self.user = User.objects.create(
            name="John Doe", email="jd@bu.edu", password="1234"
        )

        self.sellerProfile1 = SellerProfile.objects.create(
            user=self.user, phone="1234567890"
        )

        self.item1 = Item.objects.create(
            name="Test Item 1",
            location="Test Location",
            description="This is a description of the test item1",
            seller_id=self.sellerProfile1,  # Assuming seller_id is an instance of User
            category_id=None,  # Assuming category_id can be null
            price=100.0,
            image="path/to/image.jpg",
        )
        self.item2 = Item.objects.create(
            name="Test Item 2",
            location="Test Location2",
            description="This is a description of the test item2",
            seller_id=self.sellerProfile1,  # Assuming seller_id is an instance of User
            category_id=None,  # Assuming category_id can be null
            price=50.0,
            image="path/to/image.jpg",
        )

        self.cart = Cart.objects.create(user_id=self.user, item_id=self.item1)
        self.cart = Cart.objects.create(user_id=self.user, item_id=self.item2)

    def test_show_items_in_cart(self):
        # Assume you have a URL path 'show_items_in_cart' to get items in cart
        # patch HttpRequest.session to return a user_id
        session = {'user_id': self.user.id}
        with patch.object(db, "SessionStore", return_value=session):
            url = "/api/show-items-in-cart/"
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['cart'][0]['name'], self.item1.name)
            self.assertEqual(response.json()['cart'][1]['name'], self.item2.name)
            self.assertEqual(
                response.json()['cart'][0]['description'], self.item1.description
            )
            self.assertEqual(
                response.json()['cart'][1]['description'], self.item2.description
            )
            self.assertEqual(response.json()['cart'][0]['price'], self.item1.price)
            self.assertEqual(response.json()['cart'][1]['price'], self.item2.price)
            self.assertEqual(response.json()['cart'][0]['seller_user_name'], "John Doe")
            self.assertEqual(response.json()['cart'][1]['seller_user_name'], "John Doe")
            self.assertEqual(response.json()['amount'], 2)
            self.assertEqual(response.json()['total_price'], 150)

        # More assertions can be added here to check other item information in the response
