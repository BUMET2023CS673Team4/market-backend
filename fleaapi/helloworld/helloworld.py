from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def helloworld(request: HttpRequest) -> HttpResponse:
    """
    Sample API endpoint that returns a JSON response.
    """
    return JsonResponse({"message": "Hello, world!"})
