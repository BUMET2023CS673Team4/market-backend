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
from django.urls import include, path, re_path
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

# Debug React proxy
if settings.DEBUG:
    from .frontend import CSRFedDebugReactProxyView

    urlpatterns.extend(
        [
            re_path(r'^(?P<path>.*)$', CSRFedDebugReactProxyView),
        ]
    )
else:
    from .frontend import nonroot_static, react, root_static

    # Keep this section in sync with frontent/src/App.js
    urlpatterns.extend(
        [
            path("", react),
            path("signin", react),
            path("signup", react),
            path("forgotpassword", react),
            path("product/electronics", react),
            path("product/textbooks", react),
            path("product/funiture", react),
            path("product/electronics/productlist", react),
            path("product/funiture/productlist", react),
            path("product/textbooks/productlist", react),
            path("product/electronics/details", react),
            path("forgotpassword", react),
            path("checkout", react),
            re_path(r'^(?P<path>static/.*)$', root_static),
            path("favicon.ico", nonroot_static),
            path("logo192.png", nonroot_static),
            path("logo512.png", nonroot_static),
            path("robots.txt", nonroot_static),
        ]
    )
