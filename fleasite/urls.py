"""
URL configuration for flea project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.static import serve


# for test only
@ensure_csrf_cookie
def checkout_demo_page(request):
    return serve(request, "checkout.html", document_root=settings.STATIC_ROOT)


# for test only
@ensure_csrf_cookie
def return_demo_page(request):
    return serve(request, "return.html", document_root=settings.STATIC_ROOT)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("fleaapi.urls")),
    path("checkout.html", checkout_demo_page),  # for test only
    path("return.html", return_demo_page),  # for test only
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
