from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from user_admin.models import Post, Order, Marketer, Advt

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.core import serializers
from django.template.loader import get_template

import pdfkit


from .forms import AccountantLoginForm, AccountantAuth, MarketerCreateForm
from marketer.forms import SaveOrderUpdateForm

from .decorators import should_be_accountant

from user_admin.models import Marketer


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
                return redirect("accountant_view_ads")
        else:
            print("Form invalid")
            messages.add_message(request, messages.ERROR, "Invalid username/password")
            return redirect("accountant_login")
    else:
        context["form"] = form
        return render(request, "accountant/accountant_login.html", context)

@should_be_accountant()
def accountant_view_ads(request):
    context = {}
    name        =   request.user.first_name
    marketers   =   Marketer.objects.all()
    context = {
        "name":name,
        "marketers":marketers
    }

    return render(request, "accountant/accountant_view_ad_by_marketer.html", context)


@should_be_accountant()
def accountant_logout(request):
    logout(request)
    return redirect("accountant_login")

# Ajax Request
@should_be_accountant()
def accountant_view_all_ads(request):
    response = {}
    context = {}
    
    orders = Order.objects.exclude(order_status=Order.Status.FRESH)
    print(orders)
    context["orders"] = orders
    html = render_to_string("accountant/view_all_ads.html", context, request=request)
    # queryset_json = serializers.serialize('json', orders)
    return JsonResponse({"html": html})

# Ajax Request
@should_be_accountant()
def accountant_search_ads(request):
    response = {}
    context = {}
    marketer_id = request.POST.get("marketer_id")
    
    marketer = get_object_or_404(Marketer, id=marketer_id)
    orders = Order.objects.filter(marketer_id=marketer).exclude(order_status=Order.Status.FRESH)

    print(orders)
    context["orders"] = orders
    html = render_to_string("accountant/view_all_ads.html", context, request=request)
    # queryset_json = serializers.serialize('json', orders)
    return JsonResponse({"html": html})




@should_be_accountant()
def accountant_create_marketer(request):
    if request.method == "POST":
        pass
        form = MarketerCreateForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            marketer = form.save(commit=False)
            marketer.set_password(password)
            marketer.save()
            messages.add_message(request, messages.SUCCESS, "Marketer is creted successfully")


        else:
            print("Is invaid")
            messages.add_message(request, messages.ERROR, form.errors)
    else:
        form = MarketerCreateForm()
    context = {
        "form": form
    }
    return render(request, "accountant/create-marketer.html", context)

@should_be_accountant()
def accountant_edit_order(request, order_id):
    context = {}
    order = get_object_or_404(Order, order_id = order_id)
    context["order"] = order
    orderviewform   =   SaveOrderUpdateForm(instance = order)
    context["orderviewform"] = orderviewform
    return render(request, "accountant/accountant_view_order.html", context)


@should_be_accountant()
def accountant_confirm_payment(request):
    try:
        response = {}
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, order_id=order_id)
        order.order_status = Order.Status.ACCEPTED
        order.bill_status = True
        order.save()
    except Exception as e:
        response["result"] = False
        response["msg"] = e
    response["result"] = True
    response["msg"] = "Payment Successfully Confirmed!"
    return JsonResponse(response)

@should_be_accountant()
def accountant_decline_payment(request):
    pass

@should_be_accountant()
def accountant_generate_order_bill(request, order_id):
    order = get_object_or_404(Order, order_id = order_id)
    client_name = order.client_id.name
    template = get_template ('accountant/demo_bill.html')
    html = template.render (
        {
            'order': order,
        })
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8"
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="Bill-Receipt.pdf"'
    return response


@should_be_accountant()
def accountant_decline_payment(request):
    try:
        response = {}
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, order_id=order_id)
        order.order_status = Order.Status.REJECTED
        order.bill_status = False
        order.save()
    except Exception as e:
        response["result"] = False
        response["msg"] = e
    response["result"] = True
    response["msg"] = "Order Payment Status Set to NOT Received!"
    return JsonResponse(response)

