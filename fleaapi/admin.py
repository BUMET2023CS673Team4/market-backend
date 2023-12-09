from django.contrib import admin

from .models import Cart, Category, Item, Order, SellerProfile, User

# Register your models here.

admin.site.register(User)
admin.site.register(SellerProfile)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
