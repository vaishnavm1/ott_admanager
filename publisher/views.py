from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from user_admin.models import Post, Publisher, Order, Advt

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm


from datetime import datetime

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
    context = {}
    id = request.user.id
    publisher = get_object_or_404(Publisher, id=id)
    # orders  =   Order.objects.filter(bill_status=True).exclude(signed_release_order="")
    advts   =   Advt.objects.filter(order_id__bill_status = True).exclude(order_id__signed_release_order="").filter(is_published = False)
    context = {
        "publisher": publisher,
        "advts": advts
    }
    return render(request,"publisher/publisher_home.html", context)

@should_be_publisher()
def publisher_logout(request):
    logout(request)
    return redirect("publisher_login")

@should_be_publisher()
def publisher_publish_ad(request):
    response = {}
    ad_id = request.POST.get("ad_id")
    try:
        advt = get_object_or_404(Advt, id=ad_id)
        advt.is_published = True
        advt.ad_pub_actual_date = datetime.now()
        advt.save()
        response["result"]  = True
        response["msg"] = "Ad was successfully published!"
    except Exception as e:
        response["result"]  = False
        response["msg"] = e
    return JsonResponse(response)