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
        user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
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

def logout_page(request):
    logout(request)
    return redirect('/')


def register_page(request):
    if request.user.is_authenticated:
        return redirect(main_page)
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


# INFO GATHERING
def info_gathering_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            age = request.POST.get('age')
            weight = request.POST.get('weight')
            height = request.POST.get('height')
            gender = request.POST.get('gender')
            preference = request.POST.get('preference')
            user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
            user_info.age = age
            user_info.weight = weight
            user_info.height = height
            user_info.gender = gender
            user_info.preference = preference
            user_info.save()
            return redirect(main_page)
        return render(request, "info_gathering_page.html")
    return redirect(main_page)


def settings_page(request):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
        return render(request, 'settings_page.html', {'user_info':user_info})
    return redirect(main_page)

def edit_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            age = request.POST.get('age')
            weight = request.POST.get('weight')
            height = request.POST.get('height')
            gender = request.POST.get('gender')
            preference = request.POST.get('preference')
            user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
            user_info.age = age
            user_info.weight = weight
            user_info.height = height
            user_info.gender = gender
            user_info.preference = preference
            user_info.save()
            return redirect(main_page)
        return render(request, "edit_page.html")
    return redirect(main_page)

def disableNotifications(request):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))
        user_info.telegram_id = 0
        user_info.save()
        return redirect(settings_page)
    return redirect(main_page)

def generated_mealPlan_page(request):
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=User.objects.get(username=request.user))

