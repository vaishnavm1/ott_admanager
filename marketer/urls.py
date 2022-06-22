from django.contrib import admin
from django.urls import path, include

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Auth
    path('', views.marketer_login, name="marketer_login"),
    path('logout', views.marketer_logout, name="marketer_logout"),


    path('home/', views.marketer_home, name="marketer_home"),
    path('add-client/', views.marketer_add_client, name="marketer_add_client"),


    # Manage Ads
    path('add-ad/', views.marketer_add_ad, name="marketer_add_ad"),

    path('save-ad/', views.marketer_save_ad, name="marketer_save_ad"),
    
] 
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)