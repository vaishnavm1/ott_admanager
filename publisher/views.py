from django.shortcuts import render, redirect
from django.http import HttpResponse
from user_admin.models import Post

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm


from .decorators import should_be_publisher

def publisher_login(request):
    context = {}
    form = AuthenticationForm()
    if request.method == "POST":
        print("Post request")
        form = AuthenticationForm(request = request, data = request.POST)
        if form.is_valid():
            print("Valid form")
            print(form.cleaned_data.items())
            email    =   form.cleaned_data["username"]
            password     =   form.cleaned_data["password"]
            print(f"Username : {email} Password : {password}")
            user         =   authenticate(email = email, password = password)
            if(user.is_publisher):
                login(request, user)
                return redirect("publisher_home")
            else:
                print("Not a valid publisher")
        else:
            print("Form invalid")
    else:
        context["form"] = form
        return render(request, "publisher/publisher_login.html", context)

@should_be_publisher()
def publisher_home(request):
    return render(request,"publisher/publisher_home.html")

@should_be_publisher()
def publisher_logout(request):
    logout(request)
    return redirect("publisher_login")