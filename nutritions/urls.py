from django.contrib import admin
from django.urls import path
from nutritions import views

urlpatterns = [
    path('', views.main_page ),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
]
