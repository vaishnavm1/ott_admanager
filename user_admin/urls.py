from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # Auth
    path('', views.user_admin_login, name="user_admin_login"),
    path('logout/', views.user_admin_logout, name="user_admin_logout"),
    path('edit-details/', views.view_admin_edit_form, name="view_admin_edit_form"),
    path('edit/', views.edit_admin_details, name="edit_admin_details"),

    # Reset password of admin
    path('reset-password/', views.admin_reset_password, name="admin_reset_password"),



    path('home/', views.user_admin_home, name="user_admin_home"),
    path("view-posts/", views.view_posts, name="view_posts"),
 
    # Search Orders & Download PDF
    path("search-orders/", views.user_admin_search_orders, name="user_admin_search_orders"),
    path("download-orders/", views.download_order_to_pdf, name="download_order_to_pdf"),

    # Search Marketer's Clients
    path("marketer/clients-search/", views.search_marketers_clients, name="search_marketers_clients"),

    # View Discount requests
    path("view-all-discount-requests/", views.view_all_discount_requests, name="view_all_discount_requests"),
    
    # View Gst Relax requests
    path("view-all-gst-relax-requests/", views.view_all_gst_relax_requests, name="view_all_gst_relax_requests"),


    # Search for Discount requests
    path("search-discount-requests/", views.search_discount_requests, name="search_discount_requests"),

    # Search for Gst Relax requests
    path("search-gst-relax-requests/", views.search_gst_relax_requests, name="search_gst_relax_requests"),
    

    # Allow/Reject Discount
    path("allow-discount-to-client/", views.grant_discount_to_client, name="grant_discount_to_client"),

    path("reject-discount-to-client/", views.reject_discount_request, name="reject_discount_request"),
    
    
    # Allow/Reject Gst Relax Request
    path("allow-gst-relax-to-client/", views.accept_gst_relax_request, name="accept_gst_relax_request"),
    path("reject-gst-relax-to-client/", views.reject_gst_relax_request, name="reject_gst_relax_request"),

    # path("reject-discount-to-client/", views.reject_discount_request, name="reject_discount_request"),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)
