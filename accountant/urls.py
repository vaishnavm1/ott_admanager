from django.contrib import admin
from django.urls import path, include

from . import views

app_name = "accountant"

urlpatterns = [
    path('', views.accountant_login, name="accountant_login"),
    path('view-ads/', views.accountant_view_ads, name="accountant_view_ads"),

    path('logout', views.accountant_logout, name="accountant_logout"),

    path('create-marketer/', views.accountant_create_marketer, name="accountant_create_marketer"),


    # Ajax
    path('acc/view-all-ads', views.accountant_view_all_ads, name="accountant_view_all_ads"),
    
    
    # Ajax
    path('acc/search-ads', views.accountant_search_ads, name="accountant_search_ads"),


    # View order details
    path('acc/view-order/<str:order_id>', views.accountant_edit_order, name="accountant_edit_order"),

    
    
    # Cofirm order's payment
    path('acc/order/confirm-payment', views.accountant_confirm_payment, name="accountant_confirm_payment"),

    path('acc/order/generate-bill-receipt/<str:order_id>', views.accountant_generate_order_bill, name="accountant_generate_order_bill"),


    # path("view-pics", views.accountant_)
]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)