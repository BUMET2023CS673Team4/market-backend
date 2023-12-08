# from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect


def request_password_reset(request):
    if request.method == "POST":
        email = request.POST["email"]
        try:
            user = User.objects.get(email=email)
            # If user exists, redirect to reset password page
            return redirect('reset-password')
        except User.DoesNotExist:
            return HttpResponse("User with the provided email does not exist.", status=404)

    # If not POST or if there are any other issues:
    return HttpResponse(status=400)


def reset_password(request):
    if request.method == "POST":
        email = request.POST["email"]
        new_password = request.POST["new_password"]
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return HttpResponse("Password successfully changed.", status=200)
        except User.DoesNotExist:
            return HttpResponse("User with the provided email does not exist.", status=404)

    # If not POST or if there are any other issues:
    return HttpResponse(status=400)