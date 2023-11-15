"""
This file is a site-level script to reverse-proxy the frontend server. It will only be used in development mode.
Change the upstream as needed but do not commit the change.
"""
from django.views.decorators.csrf import ensure_csrf_cookie
from revproxy.views import ProxyView


class DebugReactProxyView(ProxyView):
    upstream = "http://localhost:3000/"


@ensure_csrf_cookie
def CSRFedDebugReactProxyView(request, *args, **kwargs):
    return DebugReactProxyView.as_view()(request, *args, **kwargs)
