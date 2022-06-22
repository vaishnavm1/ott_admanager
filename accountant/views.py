from django.shortcuts import render, redirect
from django.http import HttpResponse
from user_admin.models import Post

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import AccountantLoginForm, AccountantAuth

from .decorators import should_be_accountant


def accountant_login(request):
    context = {}
    form = AuthenticationForm()
    if request.method == "POST":
        print("Post request")
        form = AuthenticationForm(request = request, data = request.POST)
        if form.is_valid():
            print(form.cleaned_data.items())
            email    =   form.cleaned_data["username"]
            password     =   form.cleaned_data["password"]
            print(f"Username : {email} Password : {password}")
            user         =   authenticate(email = email, password = password)
            if(user.is_accountant):
                login(request, user)
                return redirect("accountant_home")
        else:
            print("Form invalid")
            messages.add_message(request, messages.ERROR, "Invalid username/password")
            return redirect("accountant_login")
    else:
        context["form"] = form
        return render(request, "accountant/accountant_login.html", context)

@should_be_accountant()
def accountant_home(request):
    context = {}
    return render(request, "accountant/accountant_home.html", context)

@should_be_accountant()
def accountant_logout(request):
    logout(request)
    return redirect("accountant_login")

