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

from datetime import datetime

from .forms import AccountantLoginForm, AccountantAuth, MarketerCreateForm, EditMarketerForm
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
            marketer.is_marketer = True
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
def accountant_edit_marketers(request):
    context = {}
    marketers = Marketer.objects.all()
    context["marketers"] = marketers
    return render(request, "accountant/accountant_edit_marketers.html", context)


@should_be_accountant()
def accountant_edit_marketer(request, id):
    context = {}
    marketer = get_object_or_404(Marketer, id=id)
    # if request.method == "POST":
    #     form = EditMarketerForm(instance = marketer, data = request.POST)
    form = EditMarketerForm(instance = marketer)
    context["id"] = marketer.id
    context["name"] = marketer
    context["is_active"] = marketer.is_active
    context["form"] = form
    # return HttpResponse(f"Ok Editing {id}")
    return render(request, "accountant/accountant_marketer_edit.html", context)

# Ajax view
@should_be_accountant()
def edit_marketer(request,id):
    context = {}
    if request.method == "POST":
        marketer = get_object_or_404(Marketer, id=id)
        form = EditMarketerForm(instance = marketer, data = request.POST)
        if form.is_valid():
            form.save()
            context["result"] = True
            context["msg"] = "Marketer details has been edited!"
            return JsonResponse(context)
        else:
            context["result"] = False
            context["msg"] = "Error in Form"
            return JsonResponse(context)

# Ajax View
@should_be_accountant()
def reset_marketer_password(request):
    context = {}
    if request.method == 'POST':
        new_password = request.POST.get('new_password', None)
        confirm_new_password = request.POST.get('confirm_new_password', None)
        if new_password == None or confirm_new_password == None:
            context["result"] = False
            context["msg"] = "Please enter new & confirm new password"
            return JsonResponse(context)

        if new_password != confirm_new_password:
            context["result"] = False
            context["msg"] = "Cofirm & New passwords should be same"
            return JsonResponse(context)
        id = request.POST.get("id", None)
        marketer = get_object_or_404(Marketer, id=id)
        marketer.set_password(new_password)
        marketer.save()
        context["result"] = True
        context["msg"] = "Password has been changed successfully!"
        return JsonResponse(context)


    return JsonResponse(context)

# Ajax view
@should_be_accountant()
def deactivate_marketer_account(request):
    context = {}
    try:
        id = request.POST.get("id", None)
        marketer = get_object_or_404(Marketer, id=id)
        marketer.is_active = False
        marketer.save()
        context["msg"] = "Marketer account has been deactivated successfully"
        context["result"] = True
        return JsonResponse(context)
    except:
        context["msg"] = "Error in deactivating marketer account"
        context["result"] = False
        return JsonResponse(context)




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
        
        # if order.gst_relax_decision == False:
        #     order.gst_amount = order.gst_final_bill_amt

        # if(order.discount_decision == True):
        #     if((order.total_bill_amt - order.discount_alloted_amt)== order.discounted_new_bill_amt):
        #         order.final_bill_amt = order.discounted_new_bill_amt
        # else:
        #     order.final_bill_amt = order.total_bill_amt
        #     print("Discount not given & final amt set to total bill amt")
        # Add current datetime when accountant accepted payment, to add in Bill
        order.payment_accepted_datetime = datetime.now()
        order.save()
    except Exception as e:
        response["result"] = False
        response["msg"] = e
    response["result"] = True
    response["msg"] = "Payment Successfully Confirmed!"
    return JsonResponse(response)

@should_be_accountant()
def accountant_decline_payment(request):
    try:
        response = {}
        order_id = request.POST.get('order_id')
        rej_msg = request.POST.get('reject_msg')
        order = get_object_or_404(Order, order_id=order_id)
        order.order_status = Order.Status.REJECTED
        order.bill_status = False
        order.bill_status_msg = rej_msg
        # if(order.discount_decision == True):
        #     if((order.total_bill_amt - order.discount_alloted_amt)== order.discounted_new_bill_amt):
        #         order.final_bill_amt = order.discounted_new_bill_amt
        # else:
        #     order.final_bill_amt = order.total_bill_amt
        #     print("Discount not given & final amt set to total bill amt")
        
        order.save()
    except Exception as e:
        response["result"] = False
        response["msg"] = e
    response["result"] = True
    response["msg"] = "Payment has been Declined!"
    return JsonResponse(response)

def formatINR(number):
    s, *d = str(number).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)

import decimal    

def num2words(num):
    num = decimal.Decimal(num)
    decimal_part = num - int(num)
    num = int(num)

    if decimal_part:
        return num2words(num) + " point " + (" ".join(num2words(i) for i in str(decimal_part)[2:]))

    under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakhs', 10000000: 'Crores'}

    if num < 20:
        return under_20[num]

    if num < 100:
        return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

    # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
    pivot = max([key for key in above_100.keys() if key <= num])
    return num2words(num // pivot) + ' ' + above_100[pivot] + ('' if num % pivot==0 else ' ' + num2words(num % pivot))


from django.template.loader import get_template
import imgkit
import json
import base64
import requests

@should_be_accountant()
def accountant_generate_order_bill(request, order_id):
    order = get_object_or_404(Order, order_id = order_id)
    client_name = order.client_id.name
    template = get_template ('accountant/bill.html')

    final_bill_amt = formatINR(order.final_bill_amt)
    gst_final_bill_amt = order.gst_final_bill_amt

    if(order.discount_decision == True):
        # Total - Discount = Gross Amt
        gross_amt = order.total_bill_amt - order.discount_alloted_amt
        template_context = {
            'order': order,
            "client_name": client_name,
            "final_bill_amt" : final_bill_amt,
            "discounted_amt": formatINR(order.discount_alloted_amt),
            "gross_amt": formatINR(gross_amt)
        }
    else:
        template_context = {
            'order': order,
            "client_name": client_name,
            "final_bill_amt" : final_bill_amt
        }
    if order.client_id.agency_id != None:
        template_context["agency_discount_amt"] = formatINR(order.agency_discount_amt)

    num_to_words_amt = num2words(gst_final_bill_amt)
    print(f"Gst : {gst_final_bill_amt} Final Bill : {order.final_bill_amt}")

    template_context["gst_amt"] = formatINR(gst_final_bill_amt - order.final_bill_amt)
    template_context["final_bill_amt"] = formatINR(order.final_bill_amt)
    template_context['total_bill_amt'] = formatINR(order.total_bill_amt)
    template_context['gst_final_bill_amt'] = formatINR(gst_final_bill_amt)
    template_context['final_amt_words'] = num_to_words_amt

    html = template.render (template_context)

    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8"
    }

    print("Ok came till here...")
    url = "http://159.223.76.134/generate-bill/"
    res = requests.post(url, data = {'pdf_string': html})
    print("came till content...")
    resp_json = json.loads(res.content)
    base64_data = resp_json['response']
    

    print(f"Response b64 size : {len(base64_data)}")

    xxx = base64.b64decode(base64_data)
    

    dump = HttpResponse(xxx, content_type='application/pdf')
    dump['Content-Disposition'] = 'attachment;filename="OTT-Invoice.pdf"'
    return dump

    exit()

    # pdf = pdfkit.from_string(html, False, options)
    # response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment;filename="Bill-Receipt.pdf"'
    # return response


# @should_be_accountant()
# def accountant_decline_payment(request):
#     try:
#         response = {}
#         order_id = request.POST.get('order_id')
#         order = get_object_or_404(Order, order_id=order_id)
#         order.order_status = Order.Status.REJECTED
#         order.bill_status = False
#         order.save()
#     except Exception as e:
#         response["result"] = False
#         response["msg"] = e
#     response["result"] = True
#     response["msg"] = "Order Payment Status Set to NOT Received!"
#     return JsonResponse(response)


# Edit Views
@should_be_accountant()
def get_marketer_dtls(request):
    response = {}
    response["msg"] = "Ok"
    return JsonResponse(response)