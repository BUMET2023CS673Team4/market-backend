from django.db import models


# List of models
# Ref: https://docs.djangoproject.com/en/4.1/topics/db/models/
# Ref: https://docs.djangoproject.com/en/4.1/ref/models/fields/


class User(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=255)


class SellerProfile(models.Model):
    id = models.AutoField(primary_key=True)
    # OneToOneField is a one-to-one relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    seller_id = models.ForeignKey(
        SellerProfile, max_length=255, on_delete=models.CASCADE
    )
    category_id = models.ForeignKey(
        Category, blank=True, max_length=255, on_delete=models.SET_NULL, null=True
    )
    price = models.FloatField()
    image = models.CharField(max_length=255) # path only, not the image itself
    date_added = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, max_length=255, on_delete=models.CASCADE)
    item_id = models.ForeignKey(
        Item, max_length=255, on_delete=models.SET_NULL, null=True
    )


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, max_length=255, on_delete=models.CASCADE)
    item_id = models.ForeignKey(
        Item, max_length=255, on_delete=models.SET_NULL, null=True
    )
    pickup_option = models.CharField(max_length=255)
    payment = models.CharField(max_length=255)
