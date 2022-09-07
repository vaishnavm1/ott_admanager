from django.contrib import admin
from django.urls import path, include

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "marketer"

urlpatterns = [
    # Auth
    path('', views.marketer_login, name="marketer_login"),
    path('logout', views.marketer_logout, name="marketer_logout"),


    path('home/', views.marketer_home, name="marketer_home"),
    path('add-client/', views.marketer_add_client, name="marketer_add_client"),
    
    # Add client Ajax url
    path('insert-client/', views.add_client, name="add_client"),


    # Add Agency
    path('add-agency/', views.marketer_add_agency, name="marketer_add_agency"),


    # Manage Ads
    path('add-ad/', views.marketer_add_ad, name="marketer_add_ad"),

    # First version [For multiple type ads]
    path('save-ad/', views.marketer_save_ad, name="marketer_save_ad"),

    # Second version [For only single ads]
    # path('save-ad-2/', views.marketer_save_ad2, name="marketer_save_ad2"),
    

    # Manage Cart
    path('view-cart/<str:order_id>', views.marketer_view_cart, name="marketer_view_cart"),

    # Get client's un-processed order
    path('get-client-order/', views.get_client_order, name="get_client_order"),

    # Delete Advt
    path('delete-advt/', views.delete_advt, name="delete_advt"),

    # Save Order
    path('order-save/', views.marketer_save_order, name="marketer_save_order"),

    # Discount urls
    path('marketer-request-discount/', views.marketer_request_discount, name="marketer_request_discount"),

    # GST urls
    path('marketer-request-gst-relax/', views.marketer_request_gst_relax, name="marketer_request_gst_relax"),


    # Generate RO
    path('generate-ro/<str:order_id>', views.generate_ro, name="generate_ro"),
    
    # Request for RO
    path('request-generate-ro/<str:order_id>', views.request_release_order, name="request_release_order"),


    # Test Ajax request
    path('test-ajax', views.test_ajax, name="test_ajax"),



    # Edit Add View
    path('edit-ads/', views.marketer_edit_ads, name="marketer_edit_ads"),

    path('search-order/', views.marketer_search_order, name="marketer_search_order"),
    
    # Edit single Ad b4 publishing it
    path('edit-ad/<int:ad_id>', views.marketer_edit_ad, name="marketer_edit_ad"),

    # Manage RO & Orders
    path('manage-ro/', views.marketer_manage_ro, name="marketer_manage_ro"),
    
    path('view-all-ro/', views.marketer_get_all_ro, name="marketer_get_all_ro"),


    path('marketer/edit-order/<str:order_id>', views.marketer_edit_order, name="marketer_edit_order"),


    path('marketer/upload-ro/<str:order_id>', views.marketer_upload_ro_image, name="marketer_upload_ro_image"),

] 
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)