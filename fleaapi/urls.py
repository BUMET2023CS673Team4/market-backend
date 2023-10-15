from django.urls import path

from . import views
from .controllers import user


urlpatterns = [
    path("helloworld/", views.helloworld),
    path("signup/", user.signup),
    path("login/", user.login),
]
