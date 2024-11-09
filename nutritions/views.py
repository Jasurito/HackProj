from django.shortcuts import render, redirect
from django.template.context_processors import request

from .models import UserInfo, User, UserSchedule
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout


def main_page(request):
    if request.user.is_authenticated:
        print(request.user.is_authenticated)
        print(request.user)
        print(request.user.id)
        print(UserInfo.objects.all())
        user_info = UserInfo.objects.filter(user=request.user).values()
        print(user_info)
        return render(request, "main_page.html", {'user_info': user_info})
    return render(request, "main_page.html", {'user_info': 'noinfo'})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # Redirect to a home page or desired page after login
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            user_instance = UserInfo.objects.create(user=user)
            UserSchedule.objects.create(user_info=user_instance)
            login(request, user)  # Automatically log in the user after registration
            return redirect('/')  # Redirect to a homepage after registration

    return render(request, 'registration.html')






