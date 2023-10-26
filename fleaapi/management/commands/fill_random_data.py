from django.core.management.base import BaseCommand
from fleaapi.models import *
import random
import string


class Command(BaseCommand):
    help = 'Fill random data into the database. Please refer to the source code for the details or for changing parameters.'

    def random_str(self, length):
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(length)
        )

    _USER_COUNT = 100
    _USER_NAME_LENGTH = 10
    _USER_PASSWORD_LENGTH = 10
    _USER_EMAIL_PREFIX_LENGTH = 5
    _USER_EMAIL_SUFFIX = "@bu.edu"

    def create_users(self):
        users = []
        for i in range(self._USER_COUNT):
            name = self.random_str(self._USER_NAME_LENGTH)
            password = self.random_str(self._USER_PASSWORD_LENGTH)
            email = name[: self._USER_EMAIL_PREFIX_LENGTH] + self._USER_EMAIL_SUFFIX
            user = User.objects.create(
                name=name,
                email=email,
                password=password,
            )
            try:
                user.full_clean()
                user.save()
                users.append(user)
            except:
                pass

        return users

    _SELLERPROFILE_COUNT = 50
    _SELLERPROFILE_PHONE_MIN = 1000000000
    _SELLERPROFILE_PHONE_MAX = 9999999999

    def create_seller_profiles(self, users):
        seller_profiles = []
        for i in range(self._SELLERPROFILE_COUNT):
            user = users[i]
            phone = random.randint(
                self._SELLERPROFILE_PHONE_MIN, self._SELLERPROFILE_PHONE_MAX
            )
            seller_profile = SellerProfile.objects.create(
                user=user,
                phone=phone,
            )
            try:
                seller_profile.full_clean()
                seller_profile.save()
                seller_profiles.append(seller_profile)
            except:
                pass

        return seller_profiles

    _CATEGORY_COUNT = 10
    _CATEGORY_NAME_LENGTH = 10

    def create_categories(self):
        categories = []
        for i in range(self._CATEGORY_COUNT):
            name = self.random_str(self._CATEGORY_NAME_LENGTH)
            category = Category.objects.create(
                name=name,
            )
            try:
                category.full_clean()
                category.save()
                categories.append(category)
            except:
                pass

        return categories

    _ITEM_COUNT = 1000
    _ITEM_NAME_LENGTH = 10
    _ITEM_LOCATION_LENGTH = 10
    _ITEM_DESCRIPTION_LENGTH = 100
    _ITEM_PRICE_MIN = 1
    _ITEM_PRICE_MAX = 1000
    _ITEM_IMAGE_EXTENSION = ".jpg"

    def create_items(self, seller_profiles, categories):
        items = []
        for i in range(self._ITEM_COUNT):
            name = self.random_str(self._ITEM_NAME_LENGTH)
            location = self.random_str(self._ITEM_LOCATION_LENGTH)
            description = self.random_str(self._ITEM_DESCRIPTION_LENGTH)
            seller = random.choice(seller_profiles)
            category = random.choice(categories)
            price = random.randint(self._ITEM_PRICE_MIN, self._ITEM_PRICE_MAX)
            image = name + self._ITEM_IMAGE_EXTENSION
            item = Item.objects.create(
                name=name,
                location=location,
                description=description,
                seller_id=seller,
                category_id=category,
                price=price,
                image=image,
            )
            try:
                item.full_clean()
                item.save()
                items.append(item)
            except:
                pass

        return items

    def handle(self, *args, **kwargs):
        users = self.create_users()
        self.stdout.write(self.style.SUCCESS('Created {} users.'.format(len(users))))

        seller_profiles = self.create_seller_profiles(users)
        self.stdout.write(
            self.style.SUCCESS(
                'Created {} seller profiles.'.format(len(seller_profiles))
            )
        )

        categories = self.create_categories()
        self.stdout.write(
            self.style.SUCCESS('Created {} categories.'.format(len(categories)))
        )

        items = self.create_items(seller_profiles, categories)
        self.stdout.write(self.style.SUCCESS('Created {} items.'.format(len(items))))
