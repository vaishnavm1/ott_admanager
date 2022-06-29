from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from user_admin.models import Publisher


def should_be_publisher():
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # Redirect to publisher login page
                return redirect("publisher_login")
            email       =   request.user.email
            password    =   request.user.password
            try:
                publisher = Publisher.objects.get(email = email, password = password)
            except Publisher.DoesNotExist:
                return redirect("publisher_login")
            return view_func(request, *args, **kwargs)
        return wrap
    return decorator
                