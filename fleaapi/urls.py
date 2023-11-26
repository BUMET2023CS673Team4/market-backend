from django.urls import path

from fleaapi.controllers.user import request_password_reset

from . import views
<<<<<<< HEAD
from .controllers import checkout, user
=======
from .controllers import user
>>>>>>> asma-forgetpassword

urlpatterns = [
    path("helloworld/", views.helloworld),
    path("signup/", user.signup),
    path("login/", user.login),
<<<<<<< HEAD
    path("stripe-public-key/", checkout.stripe_public_key),
    path("create-checkout-session/", checkout.create_checkout_session),
    path("session-status/", checkout.session_status),
=======
    # path("forgotpassword/", user.forgotpassword),
    path('request-password-reset/', request_password_reset, name='request_password_reset'),
    path('reset-password/', user.reset_password, name='reset_password'),
>>>>>>> asma-forgetpassword
]
