from django.conf import settings
from django.views.static import serve


def index(request):
    return serve(request, "index.html", document_root=settings.FRONTEND_BUILD_ROOT)


def root_static(request, path):
    return serve(request, path, document_root=settings.FRONTEND_BUILD_ROOT)
