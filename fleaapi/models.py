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
    address = models.CharField(max_length=255)
