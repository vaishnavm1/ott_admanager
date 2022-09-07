from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


from django.template.loader import get_template
import imgkit
import json
import base64
import requests
import pdfkit

from datetime import datetime, timedelta

# Project based imports

from .models import Post, Marketer, Order, Admin, Client
from .forms import EditAdinForm

from .decorators import should_be_user_admin


def user_admin_login(request):
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
            if(user.is_user_admin):
                print("User is admin")
                login(request, user)
                return redirect("user_admin_home")
            else:
                messages.add_message(request, messages.ERROR, "Invalid username/password")
                return redirect("user_admin_login")

        else:
            messages.add_message(request, messages.ERROR, "Invalid username/password")
            return redirect("user_admin_login")
    else:
        context["form"] = form
        return render(request, "user_admin/user_admin_login.html", context)



@should_be_user_admin()
def user_admin_home(request):
    context = {}
    marketers = Marketer.objects.all()
    clients = Client.objects.all()
    dis_reqs = Order.objects.filter(discount_requested = True).filter(discount_decision = None)
    gst_relax_reqs = Order.objects.filter(gst_relax_requested = True).filter(gst_relax_decision = None)
    context = {
        "marketers": marketers,
        "clients": clients,
        "discount_requests": dis_reqs.count(),
        "gst_relax_requests": gst_relax_reqs.count(),
    }
    return render(request, "user_admin/user_admin_home.html", context)


@should_be_user_admin()
def user_admin_logout(request):
    logout(request)
    return redirect("user_admin_login")


def formatINR(number):
    s, *d = str(number).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)   


from django.core import serializers

@should_be_user_admin()
def user_admin_search_orders(request):
    response = {}
    context = {}
    start_date = request.POST.get("start_date_time")
    end_date = request.POST.get("end_date_time")
    marketer_id = request.POST.get("marketer_id")
    client_id = request.POST.get("client_id")
    
    
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d %I:%M%p')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d %I:%M%p')
    if marketer_id != "0":
        marketer = get_object_or_404(Marketer, id=marketer_id)
        queryset_orders = Order.objects.filter(marketer_id=marketer).exclude(order_status=Order.Status.FRESH)
    else:
        queryset_orders = Order.objects.all().exclude(order_status=Order.Status.FRESH)
    
    if client_id != "0":
        client = get_object_or_404(Client, id=client_id)
        queryset_orders = queryset_orders.filter(client_id = client)
    
    
    
    queryset_orders = queryset_orders.filter(created__gte=start_date_obj, created__lte=end_date_obj)
    temp = queryset_orders.values("id")
    qs_ids = []
    [qs_ids.append(t['id']) for t in temp]
    qs_ids_json = qs_ids
    
    total_orders = queryset_orders.count()
    # Order.objects.aggregate(Sum('total_bill_amt'))
    # total_orders_amt = queryset_orders.aggregate(total = Sum('final_bill_amt'))['total']
    total_orders_amt = 0
    for q in queryset_orders:
        if q.gst_relax_decision == True:
            amt = q.final_bill_amt
            total_orders_amt += amt
        else:
            if q.client_id.agency_id != None:
                amt = q.final_bill_amt
                total_orders_amt += amt
            else:
                amt = q.gst_final_bill_amt
                total_orders_amt += amt

    if total_orders_amt == None:
        total_orders_amt = 0

    context["orders"] = queryset_orders
    html = render_to_string("user_admin/view_orders.html", context, request=request)

    response = {
        "html": html,
        "total_orders": total_orders,
        "total_bill_amt": formatINR(total_orders_amt),
        "qs_ids_json": qs_ids_json
    }
    return JsonResponse(response)



@should_be_user_admin()
def download_order_to_pdf_old(request):
    context = {}
    context["msg"] = "Came till here"
    template = get_template ('user_admin/order_report.html')
    template_context = {}
    template_context["code"] = "SEcret Code"
    html = template.render (template_context)


    

    # options = {
    #     'page-size': 'Letter',
    #     'encoding': "UTF-8"
    # }
    # pdf = pdfkit.from_string(html, False, options)
    # response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment;filename="Release-Order.pdf"'
    # return response


    return JsonResponse(context)



@should_be_user_admin()
def search_marketers_clients(request):
    context = {}
    marketer_id = request.POST.get("m_id")
    marketer = get_object_or_404(Marketer, id=marketer_id)
    queryset = Client.objects.filter(marketer_id=marketer)
    context["talukas"] = queryset
    html = render_to_string("user_admin/tagify_clients.html", context, request=request)
    return JsonResponse({"form":html,"clients": list(queryset.values())})


@should_be_user_admin()
def view_all_discount_requests(request):
    context = {}
    dis_reqs = Order.objects.filter(discount_requested = True).filter(discount_decision = None)
    gst_relax_reqs = Order.objects.filter(gst_relax_requested = True).filter(gst_relax_decision = None)
    context["discount_requests"] = dis_reqs.count()
    context["gst_relax_requests"] = gst_relax_reqs.count()
    return render(request, "user_admin/user_admin_view_all_discount_reqs.html", context)


@should_be_user_admin()
def view_all_gst_relax_requests(request):
    print("Came here....$$#")
    context = {}
    dis_reqs = Order.objects.filter(discount_requested = True).filter(discount_decision = None)
    gst_relax_reqs = Order.objects.filter(gst_relax_requested = True).filter(gst_relax_decision = None)
    context["discount_requests"] = dis_reqs.count()
    context["gst_relax_requests"] = gst_relax_reqs.count()
    return render(request, "user_admin/user_admin_view_gst_relax_reqs.html", context)



@should_be_user_admin()
def search_discount_requests(request):
    response = {}
    context = {}
    viewall = request.POST.get("viewall")
    if(viewall == "true"):
        dis_reqs_orders = Order.objects.filter(discount_requested = True).filter(discount_decision = None)
        context["orders"] = dis_reqs_orders
        html = render_to_string("user_admin/ajax/view_discount_reqs.html", context, request=request)
        response["html"] = html
    else:
        pass
    return JsonResponse(response)

@should_be_user_admin()
def grant_discount_to_client(request):
    context = {}
    id = request.user.id
    admin = get_object_or_404(Admin, id=id)

    order_id = request.POST.get("order_id")
    new_discount_amt = request.POST.get("newDiscountGivenAmt")
    print(type(new_discount_amt))

    new_discount_amt = int(new_discount_amt)
    
    order = get_object_or_404(Order, order_id = order_id)

    # Check if new allowed discount is valid or not
    asked_amt = order.discount_req_amt
    total_bill_amt = order.total_bill_amt

    if((new_discount_amt > asked_amt) or (new_discount_amt > total_bill_amt)):
        # allowed amt cannot be more than orignal amount
        context["msg"] = "Invalid Amount"
        context["result"] = False
    else:
        order.discount_decision = True
        order.discount_alloted_amt = new_discount_amt
        order.discounted_new_bill_amt = (total_bill_amt - new_discount_amt)
        order.final_bill_amt = (total_bill_amt - new_discount_amt)
        order.discount_allowed_or_rejected_admin = admin
        order.save()


        # Save amount with gst included
        final_bill = order.final_bill_amt
        order.gst_final_bill_amt = final_bill + ((final_bill * 18) / 100)
        order.save()


        context["result"] = True
        context["msg"] = "Discount has been approved to the client"
    return JsonResponse(context)


@should_be_user_admin()
def reject_discount_request(request):
    context = {}
    id = request.user.id
    admin = get_object_or_404(Admin, id=id)
    try:
        order_id = request.POST.get("order_id")
        order = get_object_or_404(Order, order_id = order_id)
        order.discount_decision = False
        order.discount_allowed_or_rejected_admin = admin
        order.save()
        context["result"] = True
        context["msg"] = "Discout request has been Rejected!"
        return JsonResponse(context)
    except Exception as e:
        context["result"] = False
        context["msg"] = f"Error in Rejecting Discount {e}"
        return JsonResponse(context)
    

@should_be_user_admin()
def download_order_to_pdf(request):
    context = {}
    template_context = {}
    start_date_time = request.POST.get("down_start_date_time", None)
    end_date_time = request.POST.get("down_end_date_time", None)
    resultIds = request.POST.get("resultIds", None)
    marketer_id = request.POST.get("down_marketer", None)

    order_ids = resultIds.strip('[]').split(',')



    # print("Printing to pDF")
    # print(start_date_time)
    # print(end_date_time)
    # print(marketer_id)
    # print(resultIds)

    order_objs = Order.objects.filter(id__in = order_ids)
    
    start_date_obj = datetime.strptime(start_date_time, '%Y-%m-%d %I:%M%p')
    end_date_obj = datetime.strptime(end_date_time, '%Y-%m-%d %I:%M%p')

    start_dt_main = datetime.strftime(start_date_obj, "%d-%B-%Y %I:%M%p")
    end_dt_main = datetime.strftime(end_date_obj, "%d-%B-%Y %I:%M%p")

    template = get_template ('user_admin/order_report.html')
    template_context["order_objs"] = order_objs
    template_context["start_date_time"] = start_dt_main
    template_context["end_date_time"] = end_dt_main
    if marketer_id != "0":
        template_context["marketer"] = get_object_or_404(Marketer, id=marketer_id)



    html = template.render (template_context)

    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8"
    }
    print("Admin Printing Order Report Ok came till here...")

    url = "http://159.223.76.134/nxtnqt-create-orders-pdf/"
    res = requests.post(url, data = {'pdf_string': html})
    resp_json = json.loads(res.content)
    base64_data = resp_json['response']


    # print(f"Orignal b64 size : {resp_json['len']}")
    # print(f"Response b64 size : {len(base64_data)}")

    xxx = base64.b64decode(base64_data)
    

    dump = HttpResponse(xxx, content_type='application/pdf')
    dump['Content-Disposition'] = 'attachment;filename="OTT-Order-Report.pdf"'
    return dump



@should_be_user_admin()
def search_gst_relax_requests(request):
    response = {}
    context = {}
    viewall = request.POST.get("viewall")
    if(viewall == "true"):
        gst_relax_reqs = Order.objects.filter(gst_relax_requested = True).filter(gst_relax_decision = None)
        context["orders"] = gst_relax_reqs
        html = render_to_string("user_admin/ajax/view_gst_relax_reqs.html", context, request=request)
        response["html"] = html
    else:
        pass
    return JsonResponse(response)

@should_be_user_admin()
def accept_gst_relax_request(request):
    try:
        response = {}
        order_id = request.POST.get("order_id", None)
        id = request.user.id
        admin = get_object_or_404(Admin, id=id)
        
        order = get_object_or_404(Order, order_id = order_id)
        old_final_bill_amt = order.final_bill_amt
        total_bill_amt = order.total_bill_amt

        order.gst_relax_decision = True
        order.gst_allowed_or_rejected_admin = admin
        order.save()
        response["result"] = True
        response["msg"] = "GST Relax request has been Accepted"
        return JsonResponse(response)
    except:
        response["result"] = False
        response["msg"] = "Problem in Accepting GST Relax request"
        return JsonResponse(response)


@should_be_user_admin()
def reject_gst_relax_request(request):
    try:
        response = {}
        order_id = request.POST.get("order_id", None)
        id = request.user.id
        admin = get_object_or_404(Admin, id=id)
        
        order = get_object_or_404(Order, order_id = order_id)
        old_final_bill_amt = order.final_bill_amt
        total_bill_amt = order.total_bill_amt

        order.gst_relax_decision = False
        order.gst_allowed_or_rejected_admin = admin
        order.save()
        response["result"] = True
        response["msg"] = "GST Relax request has been Rejected"
        return JsonResponse(response)
    except:
        response["result"] = False
        response["msg"] = "Problem in Accepting GST Relax request"
        return JsonResponse(response)


@should_be_user_admin()
def view_admin_edit_form(request):
    context = {}
    id = request.user.id
    admin = get_object_or_404(Admin, id=id)
    
    dis_reqs = Order.objects.filter(discount_requested = True).filter(discount_decision = None)
    gst_relax_reqs = Order.objects.filter(gst_relax_requested = True).filter(gst_relax_decision = None)
    context["discount_requests"] = dis_reqs.count()
    context["gst_relax_requests"] = gst_relax_reqs.count()

    form = EditAdinForm(instance = admin)
    context["form"] = form
    return render(request, "user_admin/edit_admin.html", context)


@should_be_user_admin()
def edit_admin_details(request):
    context = {}
    if request.method == "POST":
        id = request.user.id
        admin = get_object_or_404(Admin, id=id)
        form = EditAdinForm(instance = admin, data = request.POST)
        if form.is_valid():
            form.save()
            context["result"] = True
            context["msg"] = "Your details has been edited successfully!"
            return JsonResponse(context)
        else:
            context["result"] = False
            context["msg"] = "Error in Form"
            return JsonResponse(context)
            
@should_be_user_admin()
def admin_reset_password(request):
    response = {}
    new_password = request.POST.get("new_password")
    confirm_new_password = request.POST.get("confirm_new_password")

    if new_password != confirm_new_password:
        response["msg"] = "New password & Confirm password should be same!"
        response["result"] = False
        return JsonResponse(response)

    admin = get_object_or_404(Admin, id=request.user.id)
    admin.set_password(new_password)
    admin.save()

    response["msg"] = "Password has been changed successfully!"
    response["result"] = True
    return JsonResponse(response)


def view_posts(request):
    posts = Post.objects.all()
    print(len(posts))
    context = {
        "posts":posts
    }
    return render(request, "user_admin/view-posts.html", context)