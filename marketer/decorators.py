from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from user_admin.models import Marketer


def should_be_marketer():
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # Redirect to marketer login page
                return redirect("marketer_login")
            # print(f"User is Auth : {request.user.is_authenticated}")
            email       =   request.user.email
            password    =   request.user.password
            try:
                marketer = Marketer.objects.get(email = email, password = password)
                # Check marketer status
                if(marketer.is_active == False):
                    return redirect("marketer_login")

            except Marketer.DoesNotExist:
                return redirect("marketer_login")
            return view_func(request, *args, **kwargs)
        return wrap
    return decorator
                