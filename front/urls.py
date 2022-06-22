from django.contrib import admin
from django.urls import path, include

from app1 import views

urlpatterns = [
    path('', views.front_home, name="front_home"),
    
]