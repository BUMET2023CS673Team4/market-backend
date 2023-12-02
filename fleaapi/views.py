# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .helloworld import *


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # 登录成功后，你可以重定向到首页或任何其他页面
            return redirect('home_page_name')
        else:
            # 如果验证失败，你可以返回一个错误消息
            return render(
                request, 'login.html', {'error': 'Invalid email or password.'}
            )
            # return HttpResponse(status=401) # Return an 'invalid login' error message.

    else:
        return render(request, 'login.html')

import uuid

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_POST


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


from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_POST


@require_POST
def reset_password(request):
    email = request.POST.get('email')
    new_password = request.POST.get('new_password')
    reset_token = request.POST.get('reset_token')  # Assuming the token is sent in the request

    # Validate the token and find the user
    try:
        user = User.objects.get(email=email)
        # Here, check if the reset_token matches what's stored for the user
        # This depends on how you've chosen to store the token
    except User.DoesNotExist:
        return HttpResponseNotFound()

    # Check if the token is valid and matches
    if not is_valid_token(user, reset_token):
        return HttpResponseBadRequest()

    # Reset the password
    user.set_password(new_password)
    user.save()

    return HttpResponse(status=200)

def is_valid_token(user, token):
    # Implement token validation logic here
    pass
