from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core import serializers

from user_admin.models import Post, Marketer, Client, AdType, Advt, Order


import pdfkit

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from django.contrib import messages

from .decorators import should_be_marketer
from .forms import AddClientForm, AddAdForm, SaveOrderUpdateForm, UpdateRoForm, UpdateAdForm
def marketer_login(request):
    context = {}
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request = request, data = request.POST)
        if form.is_valid():
            print(form.cleaned_data.items())
            email    =   form.cleaned_data["username"]
            password     =   form.cleaned_data["password"]
            print(f"Username : {email} Password : {password}")
            user         =   authenticate(email = email, password = password)
            if(user.is_marketer):
                login(request, user)
                return redirect("marketer_home")
            else:
                print("User not valid marketer")
                return redirect("/")
        else:
            print("Form Invalid")
    else:
        context["form"] = form
        return render(request, "marketer/marketer_login.html", context)


@should_be_marketer()
def marketer_logout(request):
    logout(request)
    return redirect("marketer_login")



@should_be_marketer()
def marketer_home(request):
    return redirect("marketer_add_client")
    # return render(request, "marketer/marketer_add_client.html")



@should_be_marketer()
def marketer_add_client(request):
    if request.method == "POST":
        form = AddClientForm(data = request.POST)
        if form.is_valid():
            client_obj = form.save(commit = False)
            
            if request.user.is_marketer:
                m_id = request.user.id
                marketer = get_object_or_404(Marketer, id=m_id)
                client_obj.marketer_id = marketer
                client_obj.save()
                print("Form Saved!")
                messages.success(request, 'Client Added Successfully!')
            else:
                print("Error in Form Saved")

            
    else:
        form = AddClientForm()
    context = {
        "form":form
    }
    return render(request, "marketer/marketer_add_client.html", context)


@should_be_marketer()
def marketer_add_ad(request):
    if request.method == "POST":
        pass
    else:
        id = request.user.id
        name = request.user.first_name
        marketer = get_object_or_404(Marketer, id=id)
        clients = Client.objects.filter(marketer_id=marketer)
        ad_types = AdType.objects.filter(is_active = True)

        total_ads = Advt.objects.filter(order_id__marketer_id = marketer).count()
        form = AddAdForm()
        context = {
            'clients' : clients,
            'ad_types' : ad_types,
            "form": form,
            "name": name,
            "totalAds": total_ads
        }
    return render(request, "marketer/marketer_add_ad.html", context)


@should_be_marketer()
def get_client_order(request):
    response = {}
    client_id = request.POST.get("client_id")
    id = request.user.id
    marketer = get_object_or_404(Marketer, id=id)
    client = get_object_or_404(Client, id=client_id)

    q1 = Q(client_id = client)
    q2 = Q(marketer_id = marketer)
    q3 = Q(bill_status = False)
    q4 = Q(order_status = Order.Status.FRESH)

    # order = Order.objects.filter(client_id = client).filter(marketer_id=marketer).filter(bill_status = False)
    order = Order.objects.filter(Q(q1) & Q(q2) & Q(q3) & Q(q4))
    print(f'orders : {order.count()}')
    if order.count() > 0:
        order = order.first()
        totalAds = Advt.objects.filter(order_id=order).count()
        # Order present, return order_id & total items
        response["new_created"] = False
        response["order_id"] = order.order_id
        response["totalAds"] = totalAds
        return JsonResponse(response)

    else:
        # Create new order
        
        order = Order(client_id = client, marketer_id = marketer)
        order.save()
        response["new_created"] = True
        response["order_id"] = order.order_id
        response["totalAds"] = 0
        return JsonResponse(response)





import traceback

@should_be_marketer()
def marketer_save_ad2(request):
    response = {}
    print(request.POST)
    post_data = request.POST
    images = request.FILES
    client_id = post_data.get("client")


    id = request.user.id
    marketer = get_object_or_404(Marketer, id=id)

    client = get_object_or_404(Client, id=client_id)

    ad_type_id = post_data.get("type")
    ad_datetime = post_data.get("ad-datetime")
    order_id = post_data.get("order_id")

    print(request.POST)
    

    order = get_object_or_404(Order, order_id=order_id)

    ad_rate = AdType.objects.get(id = ad_type_id).rate

    try:

        frm = AddAdForm(data = request.POST, files = request.FILES)
        adx = frm.save(commit = False)
        adx.order_id = order

        order.total_bill_amt += ad_rate
        print(ad_rate)
        order.save()
        adx.ad_pub_date = ad_datetime
        adx.client_id = client
        adx.marketer_id = marketer
        adx.save()
    except Exception as e:
        response['result'] = False
        response['msg'] = f"Error in Ad Insertion : {e}"
        return JsonResponse(response)
    response['result'] = True
    response['msg'] = "Ad Inserted"
    totalAds = Advt.objects.filter(order_id=order).count()
    response['totalAds'] = totalAds
    return JsonResponse(response)

    

@should_be_marketer()
def marketer_save_ad(request):
    response = {}
    # marketer = Marketer.objects.all().first()
    # print(dir(request))
    # print(request.POST)
    # print(request.FILES)
    # order = Order.objects.all().first()

        
    post_data = request.POST
    images = request.FILES
    cust_id = post_data.get("client")
    client = get_object_or_404(Client, id=cust_id)

    id = request.user.id
    marketer = get_object_or_404(Marketer, id=id)

    ad_pub_dates = post_data.getlist("ad-datetime")
    ad_show_times = post_data.get("selectAdShowTimes")
    ad_type_id = post_data.get("type")

    # image1 = images.getlist('ad_image')
    # print(dir(request.FILES))


    # Order.objects.annotate(num_advts=Count('advts')).filter(num_advts__gt=1)
    # [order for order in Order.objects.all() if order.advt_set.count() > 1]
    # Backup SAVER CODE FROM StackOverflow
    
    pic = request.FILES["ad_image"]
    first_time = True

    saved_image = None

    # Ver 1 
    # try:
    
    # BUG creating new order for every add addition
    # order = Order(client_id = client, marketer_id = marketer)

    # FIX find the order with FRESH status and stick that ad to it
    q1 = Q(client_id=client)
    q2 = Q(marketer_id = marketer)
    q3 = Q(order_status = Order.Status.FRESH)
    order = Order.objects.filter(Q(q1) & Q(q2) & Q(q3)).first()
    
    # all_ad_types = {}
    # ad_types_obj = AdType.objects.all()
    # for t in ad_types_obj:
    #     all_ad_types.update({t.id:[t.title, t.rate]})

    ad_rate = AdType.objects.get(id = ad_type_id).rate
    
    

    for i in range(int(ad_show_times)):

        test_date = ad_pub_dates[i]

        frm = AddAdForm(data = request.POST)
        adx = frm.save(commit = False)

        adx.order_id = order
        order.total_bill_amt += ad_rate
        print(ad_rate)
        order.save()
        adx.ad_pub_date = test_date
        adx.client_id = client
        adx.marketer_id = marketer
        # adx.ad_image = images.get('ad_image')
        if first_time:
            first_time = False
            adx.ad_image = pic
            saved_image = adx.ad_image
        else:
            adx.ad_image = saved_image
        adx.save()
        # ad_rate = all_ad_types.get(types)

    # except:
    #     response["result"] = False
    #     response["msg"] = "Error in insertion of Advt"
    #     return JsonResponse({"response":response})

    response["result"] = True
    response["msg"] = "All the Ad(s) added to cart!"
    
    total_ads = Advt.objects.filter(order_id__marketer_id = marketer).count()
    response["totalAds"] = total_ads

    
    return JsonResponse(response)

@should_be_marketer()
def marketer_view_cart(request, order_id):
    # Remove the _ at start
    order_id = order_id[1:]
    id = request.user.id
    marketer = get_object_or_404(Marketer, id=id)
    first_name = request.user.first_name

    order = get_object_or_404(Order, order_id=order_id)
    ads_obj = Advt.objects.filter(order_id=order)

    if(order.order_status != Order.Status.FRESH):
        orderviewform   =   SaveOrderUpdateForm(instance = order)
    else:
        orderviewform = None

    client_name = order.client_id.name
    context = {
        "totalAds": ads_obj.count(),
        "first_name": first_name,
        "client_name": client_name,
        "order_obj":order,
        "ads_obj": ads_obj,
        "orderviewform": orderviewform
    }
    return render(request, "marketer/marketer_view_cart.html", context)

@should_be_marketer()
def delete_advt(request):
    response = {}
    order_id = request.POST.get("order_id")
    advt_id = request.POST.get("advt_id")

       
    
    advt = get_object_or_404(Advt, id=advt_id)
    order = get_object_or_404(Order, order_id=order_id)

    if(isLastAdvt(order, advt_id)):
        # Last Ad of order so... Delete order...
        response["last_ad"] = True
        order.delete()
        advt.delete()
        
        response["result"] = True
        return JsonResponse(response)


    order.total_bill_amt -= advt.type.rate
    order.save()

    response["new_total_bill_amt"] = order.total_bill_amt
    


    advt.delete()
    response["result"] = True
    response["last_ad"] = False
    return JsonResponse(response)


def isLastAdvt(order, advt_id):
    totalAds = Advt.objects.filter(order_id = order).count()
    if totalAds == 1:
        return True
    return False








@should_be_marketer()
def marketer_save_order(request):
    response = {}
    # This will just save order from marketer's side, but not verify it..
    # It will be verified by Accountant ONLY
    order_id    =   request.POST.get("order_id")
    mode_of_pay =   request.POST.get("mode_of_pay")
    trans_id    =   request.POST.get("transaction_id")

    if trans_id == "":
        trans_id = None

    try:
        order = get_object_or_404(Order, order_id=order_id)
    except ValidationError:
        response["result"] = False
        response["msg"] = "Invalid Request"
        return JsonResponse(response)

    order.order_status = Order.Status.IN_REVIEW
    order.mode_of_pay = mode_of_pay
    print(f"MOP : {mode_of_pay}")
    print(f"MOP Object : {order.mode_of_pay}")

    print(f"Models CASH : {Order.Mop.CASH}")
    print(f"Models UPI : {Order.Mop.UPI}")
    # exit()
    if mode_of_pay != Order.Mop.CASH:
        order.trans_id = trans_id
    
    order.save()
    print(f"FINALLY {order.mode_of_pay}")
    response["result"] = True
    response["msg"] = "Order Saved! Now you Accountant will verify the payment status & notify you"
    return JsonResponse(response)


    



from django.template.loader import get_template


@should_be_marketer()
def generate_ro(request, order_id):
    print(request.get_host())
    print(request.GET)
    order = get_object_or_404(Order, order_id = order_id)
    client_name = order.client_id.name
    template = get_template ('marketer/demo.html')
    print(f"Total are : {order.advt_set.all()}")
    html = template.render (
        {
            'order': order,
            "client_name": client_name
        })
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8"
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="Release-Order.pdf"'
    return response 

    # html = '''
    # <h1>Hello OTT from Django</h1>
    # <i>Hello test</i>
    # '''
    # pdf = pdfkit.from_string(html, False)
    # response = HttpResponse(pdf,content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="release-order.pdf"'

    # return response

@should_be_marketer()
def marketer_edit_ads(request):
    approved_unsigned_orders = Order.objects.filter(bill_status=True).filter(signed_release_order="")
    id = request.user.id
    marketer = get_object_or_404(Marketer, id=id)
    name = marketer.first_name
    clients = Client.objects.filter(marketer_id=marketer)
    context = {
        "clients": clients,
        "name": name,
        "unsigned_orders": approved_unsigned_orders.count()
    }
    return render(request, "marketer/marketer_view_orders.html", context)

# Ajax
@should_be_marketer()
def marketer_search_order(request):
    response = {}
    context = {}
    id = request.user.id
    marketer = get_object_or_404(Marketer, id=id)

    client_id = request.POST.get("client_id")
    only_confirmed = request.POST.get("checkbox_value")
    only_pending = request.POST.get("pending_check_value")

    print(f"Client ID : {client_id} Checkbox : {only_confirmed} Pending {only_pending}")

    if client_id != "0":
        print("Client is not 0")
        if only_confirmed == "true":
            orders = Order.objects.filter(Q(client_id=client_id)& Q(bill_status = True))
            if only_pending == "true":
                q1 = Q(signed_release_order = "")
                orders = orders.filter(q1)
                print("Ohhhh1")
        else:
            orders = Order.objects.filter(Q(client_id=client_id)).exclude(order_status = Order.Status.FRESH)
    else:
        print("Client is 0")
        if only_confirmed == "true":
            print("all only confirmed")
            orders = Order.objects.filter(marketer_id=marketer).filter(Q(bill_status = True))
            if only_pending == "true":
                q1 = Q(signed_release_order = "")
                orders = orders.filter(q1)
                print("Ohhhh2")
        else:
            orders = Order.objects.filter(marketer_id=marketer)


    orders = [order for order in orders if order.advt_set.count() > 1]
    print(f"New Orders : {orders}")

    response["orders"] = orders
    context["orders"] = orders
    html = render_to_string("marketer/order_search_result.html", context, request=request)
    queryset_json = serializers.serialize('json', orders)

    # response["html"] = html
    # response["queryset"] = queryset_json

    return JsonResponse({"html": html})


@should_be_marketer()
def marketer_edit_ad(request, ad_id):
    context = {}
    advt = get_object_or_404(Advt, id=ad_id)
    if request.method == "POST":
        form = UpdateAdForm(instance = advt, data = request.POST, files = request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = UpdateAdForm(instance = advt)
    context["advt"] = advt
    context["form"] = form
    
    return render(request, "marketer/marketer_edit_ad.html", context)



@should_be_marketer()
def marketer_manage_ro(request):
    approved_unsigned_orders = Order.objects.filter(bill_status=True).filter(signed_release_order="")
    id = request.user.id
    marketer = get_object_or_404(Marketer, id=id)
    clients = Client.objects.filter(marketer_id=marketer)
    context = {
        "clients": clients,
        "unsigned_orders": approved_unsigned_orders.count()
    }
    return render(request, "marketer/marketer_manage_ro.html", context)

@should_be_marketer()
def marketer_get_all_ro(request):
    response = {}
    return JsonResponse(response)

@should_be_marketer()
def marketer_edit_order(request, order_id):
    context = {}
    order = get_object_or_404(Order, order_id = order_id)
    print(order.mode_of_pay)
    orderviewform   =   SaveOrderUpdateForm(instance = order)
    form = UpdateRoForm(instance = order)
    context = {
        "order": order,
        "orderviewform": orderviewform,
        "form": form
    }
    return render(request, "marketer/marketer_edit_order.html", context)

@should_be_marketer()
def marketer_upload_ro_image(request, order_id):
    if request.method == "POST":
        response = {}
        order = get_object_or_404(Order, order_id = order_id)
        form = UpdateRoForm(files = request.FILES, instance = order)
        if form.is_valid():
            order =form.save(commit = True)
            response["result"] = True
            response["msg"] = "RO was successfully uploaded!"
            return JsonResponse(response)
        else:
            response["result"] = False
            response["msg"] = "Failure in RO uploading!"
            return JsonResponse(response)

        # return redirect("/")
    
