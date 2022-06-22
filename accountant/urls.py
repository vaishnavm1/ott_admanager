from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.accountant_login, name="accountant_login"),
    path('home', views.accountant_home, name="accountant_home"),

    path('logout', views.accountant_logout, name="accountant_logout"),
    # path("view-pics", views.accountant_)
]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)