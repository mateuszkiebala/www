from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return redirect('/')
        else:
            # Return a 'disabled account' error message
            pass
    else:
        # Return an 'invalid login' error message.
        return render(request, 'login.html')


@csrf_protect
def logout_view(request):
    logout(request)
    return redirect('/')


def is_logged(request):
    if request.user.is_authenticated():
        return HttpResponse(True)
    else:
        return HttpResponse(False)