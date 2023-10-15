from django.contrib.auth import authenticate, login, logout


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(status=200)  # Redirect to a success page.
    else:
        return HttpResponse(status=401)  # Return an 'invalid login' error message.


def logout_view(request):
    logout(request)
    return HttpResponse(status=200)  # Redirect to a success page.
