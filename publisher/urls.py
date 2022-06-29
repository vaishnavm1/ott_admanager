from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.publisher_login, name="publisher_login"),
    path('home', views.publisher_home, name="publisher_home"),
    path('logout', views.publisher_logout, name="publisher_logout"),

    # Ad Publish url
    path('publish-ad', views.publisher_publish_ad, name="publisher_publish_ad"),
    
]