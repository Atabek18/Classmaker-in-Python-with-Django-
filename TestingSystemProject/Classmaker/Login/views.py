from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('TestingSystem:dashboard'))
        else:
            return HttpResponse('Authentication failed. Please check your username and password.')
    if request.user.is_authenticated:
        return redirect(reverse("TestingSystem:dashboard"))

    return render(request, 'login/login.html')


def login_required_decorator(func):
    return login_required(func, login_url='Login:login')