from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from user_admin.models import Accountant


def should_be_accountant():
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # Redirect to accountant login page
                return redirect("accountant_login")
            email       =   request.user.email
            password    =   request.user.password
            try:
                accountant = Accountant.objects.get(email = email, password = password)
                print("OkKKKK")
            except Accountant.DoesNotExist:
                return redirect("accountant_login")
            return view_func(request, *args, **kwargs)
        return wrap
    return decorator
                