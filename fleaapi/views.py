import uuid

# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .helloworld import *


@require_POST
def request_password_reset(request):
    email = request.POST.get('email')

    # Check if user exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return HttpResponseNotFound()

    # Generate a password reset token (e.g., UUID)
    reset_token = str(uuid.uuid4())

    # Save the token somewhere (e.g., in the user's profile or a separate model)

    # Send an email with the reset token or link
    send_mail(
        'Password Reset Request',
        f'Your reset token is: {reset_token}',
        'from@example.com',
        [email],
        fail_silently=False,
    )

    return HttpResponse(status=200)
