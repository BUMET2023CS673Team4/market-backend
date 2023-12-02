from django.urls import path

from . import views
from .controllers import checkout, user

urlpatterns = [
    path("helloworld/", views.helloworld),
    path("signup/", user.signup),
    path("login/", user.login),
    path("stripe-public-key/", checkout.stripe_public_key),
    path("create-checkout-session/", checkout.create_checkout_session),
    path("session-status/", checkout.session_status),
<<<<<<< HEAD
=======
    # path("forgotpassword/", user.forgotpassword),
    path('request-password-reset/', request_password_reset, name='request_password_reset'),
    path('reset-password/', user.reset_password, name='reset_password'),
>>>>>>> parent of 120a802 (Revert "updated repo folders")
]
