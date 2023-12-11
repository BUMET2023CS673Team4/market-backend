import logging

from django.db import IntegrityError
from django.forms import ValidationError
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from django.shortcuts import redirect
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
        return redirect("/signin")  # send user to signin page on successful signup
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

        if user is not None:
            # Successful login
            logger.info(f"[login] user {email} logged in successfully")
            request.session["user_id"] = user.id
            return redirect("/")  # send user to home page on successful login

    except Exception as e:
        logger.error(f"[login] failed to get user with email {email}: {repr(e)}")
        return HttpResponseBadRequest()


@require_POST
def request_password_reset(request: HttpRequest) -> HttpResponse:
    """
    Request password reset for a user.
    Endpoint: POST /api/request-password-reset/
    Post Form Data:
        email: the email of the user
    """


    email = request.POST.get("email")
    if not email:
        return HttpResponseBadRequest("Email is required.")

    try:
        user = User.objects.get(email=email)
        # Logic for sending password reset email goes here
        # For example, generate a token and send it via email
        return redirect('reset-password')  # Redirect to reset password page
    except User.DoesNotExist:
        return HttpResponse("User with the provided email does not exist.", status=404)


@require_POST
# @csrf_exempt
def reset_password(request: HttpRequest) -> HttpResponse:
    """
    Reset the password for a user.
    Endpoint: POST /api/reset-password/
    Post Form Data:
        email: the email of the user
        new_password: the new password
    """
    email = request.POST.get("email")
    new_password = request.POST.get("new_password")

    if not email or not new_password:
        return HttpResponseBadRequest("Email and new password are required.")

    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return HttpResponse("Password successfully changed.", status=200)
    except User.DoesNotExist:
        return HttpResponse("User with the provided email does not exist.", status=404)
