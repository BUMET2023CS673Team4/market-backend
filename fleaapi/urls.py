from django.urls import path

from . import views
from .controllers import user
from .controllers import homepage


urlpatterns = [
    path("helloworld/", views.helloworld),
    path("signup/", user.signup),
    path("login/", user.login),
    path('items/', homepage.get_homepage_items, name='get_homepage_items'),
    path('items/', homepage.get_category_items, name='get_category_items'),
    path('items/', homepage.search_items, name='search_items'),
    path('items/<int:item_id>/', homepage.get_item_details, name='get_item_details'),
    path('user/', homepage.get_user_info, name='get_user_info'),
    path('cart/add/', homepage.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', homepage.remove_from_cart, name='remove_from_cart'),
]
