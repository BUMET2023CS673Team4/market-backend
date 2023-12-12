"""
This file is a site-level script to reverse-proxy the frontend server. It will only be used in development mode.
Change the upstream as needed but do not commit the change.
"""
import requests
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.static import serve
from revproxy.views import ProxyView


@ensure_csrf_cookie
def react(request):
    return serve(request, "index.html", document_root=settings.FRONTEND_BUILD_ROOT)


def root_static(request, path):
    return serve(request, path, document_root=settings.FRONTEND_BUILD_ROOT)


def nonroot_static(request):
    return serve(request, request.path[1:], document_root=settings.FRONTEND_BUILD_ROOT)


class DebugReactProxyView(ProxyView):
    upstream = "http://localhost:3000/"


@ensure_csrf_cookie
def CSRFedDebugReactProxyView(request, *args, **kwargs):
    return DebugReactProxyView.as_view()(request, *args, **kwargs)


def debug_random_media_view(request, path):
    response = requests.get("https://picsum.photos/200")
    return HttpResponse(response.content, content_type="image/jpeg")
