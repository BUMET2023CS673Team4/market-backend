import logging

from django.db import IntegrityError
from django.forms import ValidationError
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from django.views.decorators.http import require_POST

from fleaapi.models import User


@require_POST
def register(request: HttpRequest) -> HttpResponse:
    ALLOWED_HOSTS = ["bu.edu"]

    logger = logging.getLogger(__name__)
    logger.info("[register] flow started")

    name = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("password")

    if not name or not email or not password:
        logger.error(f"[register] missing required fields")
        return HttpResponseBadRequest()

    logger.info(f"[register] received request for email: {email}")

    if not any([email.endswith(f"@{host}") for host in ALLOWED_HOSTS]):
        logger.error(f"[register] email {email} is not allowed")
        return HttpResponseBadRequest()

    try:
        user = User.objects.create(name=name, email=email, password=password)
        user.full_clean()
        user.save()
        logger.info(f"[register] created user: {user}")
        return HttpResponse(status=201)  # Created
    except (ValidationError, IntegrityError) as e:
        logger.error(f"[register] validate user with email {email} failed: {e}")
        return HttpResponseBadRequest()
    except Exception as e:
        logger.error(
            f"[register] create user with email {email} failed: {repr(e)}"
        )  # using repr() here so we can see the type of the exception
        return HttpResponseServerError()
