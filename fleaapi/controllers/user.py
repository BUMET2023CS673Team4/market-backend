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
def signup(request: HttpRequest) -> HttpResponse:
    """
    Sign up a new user.
    Endpoint: POST /api/signup/
    Post Form Data:
        name: the name of the user
        email: the email of the user
        password: the password of the user
    :param request: the request object
    :return: 201 if success, 400 if invalid request, 500 if internal error
    """
    ALLOWED_HOSTS = ["bu.edu"]

    logger = logging.getLogger(__name__)
    logger.info("[signup] flow started")

    name = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("password")

    if not name or not email or not password:
        logger.error(f"[signup] missing required fields")
        return HttpResponseBadRequest()

    logger.info(f"[signup] received request for email: {email}")

    if not any([email.endswith(f"@{host}") for host in ALLOWED_HOSTS]):
        logger.error(f"[signup] email {email} is not allowed")
        return HttpResponseBadRequest()

    try:
        user = User.objects.create(name=name, email=email, password=password)
        user.full_clean()
        user.save()
        logger.info(f"[signup] created user: {user}")
        return HttpResponse(status=201)  # Created
    except (ValidationError, IntegrityError) as e:
        logger.error(f"[signup] validate user with email {email} failed: {e}")
        return HttpResponseBadRequest()
    except Exception as e:
        logger.error(
            f"[signup] create user with email {email} failed: {repr(e)}"
        )  # using repr() here so we can see the type of the exception
        return HttpResponseServerError()


from django.contrib.auth import authenticate


def login(request: HttpRequest) -> HttpResponse:
    """
    Log in an existing user.
    Endpoint: POST /api/login/
    Post Form Data:
        email: the email of the user
        password: the password of the user
    :param request: the request object
    :return: 200 if success, 400 if invalid request, 401 if unauthorized, 500 if internal error
    """
    logger = logging.getLogger(__name__)
    logger.info("[login] flow started")

    email = request.POST.get("email")
    password = request.POST.get("password")

    if not email or not password:
        logger.error(f"[login] missing required fields")
        return HttpResponseBadRequest()

    # Authenticate the user
    try:
        user = User.objects.get(email=email)
        if user is None:
            logger.error(f"[login] user with email {email} does not exist")
            return HttpResponseBadRequest()
        if user.password != password:
            logger.error(f"[login] password for user {email} is incorrect")
            return HttpResponseBadRequest()
    except Exception as e:
        logger.error(f"[login] failed to get user with email {email}: {repr(e)}")
        return HttpResponseBadRequest()

    if user is not None:
        # Successful login
        logger.info(f"[login] user {email} logged in successfully")
        return HttpResponse(status=200)  # OK
    else:
        # Authentication failed
        logger.error(f"[login] authentication failed for email: {email}")
        return HttpResponse(status=401)  # Unauthorized

# 获取当前用户信息
def get_user_info(request):
    if request.user.is_authenticated:
        response_data = {
            'username': request.user.username,
            'email': request.user.email,
            # 其他字段
        }
        return JsonResponse({'status': 'success', 'user': response_data})
    else:
        return JsonResponse({'status': 'failed', 'message': 'User not authenticated'})
