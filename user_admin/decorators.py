from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from user_admin.models import Admin


def should_be_user_admin():
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # Redirect to user_admin login page
                print("Admin not authenticated!!!!")
                return redirect("user_admin_login")
            print(f"User is Auth : {request.user.is_authenticated}")
            email       =   request.user.email
            password    =   request.user.password
            try:
                admin = Admin.objects.get(email = email, password = password)
            except Admin.DoesNotExist:
                return redirect("user_admin_login")
            return view_func(request, *args, **kwargs)
        return wrap
    return decorator
                