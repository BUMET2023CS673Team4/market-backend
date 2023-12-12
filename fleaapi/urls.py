from django.urls import path

from . import views
from .controllers import cart, checkout, pages, product, user

urlpatterns = [
    path("helloworld/", views.helloworld),
    path("signup/", user.signup),
    path("login/", user.login),
    path("stripe-public-key/", checkout.stripe_public_key),
    path("create-checkout-session/", checkout.create_checkout_session),
    path("session-status/", checkout.session_status),
    path("get-product-by-id/", product.get_product_by_id),
    path("add-item-to-cart/", product.add_item_to_cart),
    path("show-items-in-cart/", cart.show_items_in_cart),
    path(
        'request-password-reset/',
        views.request_password_reset,
        name='request_password_reset',
    ),
    path('reset-password/', user.reset_password, name='reset_password'),
    path("categories/", pages.all_categories),
    path("homepage/", pages.homepage),
    path("categories/<int:category_id>/items/", pages.category_items),
]
