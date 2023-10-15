from django.shortcuts import render, redirect

from .helloworld import *

# Create your views here.
from django.contrib.auth import authenticate, login

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
            return render(request, 'login.html', {'error': 'Invalid email or password.'})
            #return HttpResponse(status=401) # Return an 'invalid login' error message.
    
    else:
        return render(request, 'login.html')
