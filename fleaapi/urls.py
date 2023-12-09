from django.urls import path

from fleaapi.controllers.user import request_password_reset

from . import views
from .controllers import checkout, user, product, cart

urlpatterns = [
    path("helloworld/", views.helloworld),
    path("signup/", user.signup),
    path("login/", user.login),
    path("stripe-public-key/", checkout.stripe_public_key),
    path("create-checkout-session/", checkout.create_checkout_session),
    path("session-status/", checkout.session_status),
    # path("forgotpassword/", user.forgotpassword),
    path('request-password-reset/', request_password_reset, name='request_password_reset'),
    path('reset-password/', user.reset_password, name='reset_password'),
    path("get-product-by-id/", product.get_product_by_id),
    path("add-item-to-cart/", product.add_item_to_cart),
    path("show-items-in-cart/", cart.show_items_in_cart),
]
