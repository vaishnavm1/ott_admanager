from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core import serializers

from django.core.exceptions import PermissionDenied

import pdfkit
from django.db import IntegrityError

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from django.contrib import messages

# from user_admin.models import Post, Marketer, Client, AdType, Advt, Order # Removed AdType
from user_admin.models import (
    Post, Marketer, Client,
    Advt, Order, Location,
    AdLoc, Type, Agency
)


# Python imports
import requests
from datetime import datetime

# Custom modules/etc imports
from .decorators import should_be_marketer
from .forms import (
    AddClientForm, AddAdForm, SaveOrderUpdateForm,
    UpdateRoForm, UpdateAdForm, AddAgencyForm
)

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
            return redirect("/")
            
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
        agency_form = AddAgencyForm()
        marketer = get_object_or_404(Marketer, id=request.user.id)
        agencies = Agency.objects.filter(marketer_id=marketer)
        
    context = {
        "form":form,
        "agency_form":agency_form,
        "agencies": agencies

    }
    return render(request, "marketer/marketer_add_client.html", context)


def validateUniqueClientEmail(email):
    q1 = Q(email = email)
    # q2 = Q(mobile_no = mobile_no)
    # q3 = Q(whatsapp_mobile_no = whatsapp_mobile_no)

    count = Client.objects.filter(Q(q1)).count()
    if count != 0:
        return False
    return True

def validateUniqueClientMbno(mobile_no):
    q1 = Q(mobile_no = mobile_no)

    count = Client.objects.filter(Q(q1)).count()
    if count != 0:
        return False
    return True

def validateUniqueClientWhatsAppMbno(whatsapp_mobile_no):
    q1 = Q(whatsapp_mobile_no = whatsapp_mobile_no)

    count = Client.objects.filter(Q(q1)).count()
    if count != 0:
        return False
    return True

def validateUniqueClientGst(gst_number):
    q1 = Q(gst_number = gst_number)

    count = Client.objects.filter(Q(q1)).count()
    if count != 0:
        return False
    return True



def validateUniqueAgencyEmail(agency_email):
    q1 = Q(agency_email = agency_email)

    count = Agency.objects.filter(Q(q1)).count()
    if count != 0:
        return False
    return True

def validateUniqueAgencyMbno(agency_mobile_no):
    q1 = Q(agency_mobile_no = agency_mobile_no)

    count = Agency.objects.filter(Q(q1)).count()
    if count != 0:
        return False
    return True

def validateUniqueAgencyWhatsAppMbno(agency_whatsapp_mobile_no):
    q1 = Q(agency_whatsapp_mobile_no = agency_whatsapp_mobile_no)

    count = Agency.objects.filter(Q(q1)).count()
    if count != 0:
        return False
    return True

def validateUniqueAgencyGst(agency_gst_number):
    q1 = Q(agency_gst_number = agency_gst_number)

    count = Agency.objects.filter(Q(q1)).count()
    if count != 0:
        return False
    return True

# Ajax view
@should_be_marketer()
def add_client(request):
    context = {}
    if request.method != "POST":
        return render(request, "marketer/marketer_add_client.html", context)
    client_type = request.POST.get("client_type", None)
    
    


    if client_type == "Direct Client":
        print("Direct client")
        m_id = request.user.id
        marketer = get_object_or_404(Marketer, id=m_id)

        client_name = request.POST.get("name", None)
        client_district = request.POST.get("district", None)
        client_taluka = request.POST.get("taluka", None)
        client_address = request.POST.get("address", None)
        client_mobile_no = request.POST.get("mobile_no", None)
        client_whatsapp_mobile_no = request.POST.get("whatsapp_mobile_no", None)
        client_gst_number = request.POST.get("gst_number", None)
        client_email = request.POST.get("email", None)
        client_company_name = request.POST.get("company_name", None)
        # client_type = Client.Type.DIRECT_CLIENT

        if validateUniqueClientEmail(client_email) == False:
            context["result"] = False
            context["message"] = "EMAIL"
            return JsonResponse(context)


        if validateUniqueClientMbno(client_mobile_no) == False:
            context["result"] = False       
            context["message"] = "MBNO"
            return JsonResponse(context)

        if validateUniqueClientWhatsAppMbno(client_whatsapp_mobile_no) == False:
            context["result"] = False       
            context["message"] = "WS_MBNO"
            return JsonResponse(context)

        if validateUniqueClientGst(client_gst_number) == False:
            context["result"] = False       
            context["message"] = "GST"
            return JsonResponse(context)


        form = AddClientForm(data = request.POST)

        if form.is_valid:
            client = form.save(commit=False)
            client.marketer_id = marketer
            client.save()
            print(form.errors)

            context["result"] = True
            context["message"] = "Client added successfully"
            return JsonResponse(context)
        else:
            context["result"] = False
            context["message"] = "Error in Client addition"
            return JsonResponse(context)

            
        

    elif client_type == "Agency":
        m_id = request.user.id
        marketer = get_object_or_404(Marketer, id=m_id)
        agency_id = request.POST.get("agency", None)

        agency = get_object_or_404(Agency, id=agency_id)
        

        form = AddClientForm(data = request.POST)

        if form.is_valid:
            client = form.save(commit=False)
            client.marketer_id = marketer
            client.agency_id = agency
            client.save()

            context["result"] = True
            context["message"] = "Client added successfully"
            return JsonResponse(context)
        else:
            context["result"] = False
            context["message"] = "Error in Client addition"
            return JsonResponse(context)
        


        
        
    else:
        context["result"] = False
        context["msg"] = "Invalid Client type"
        return JsonResponse(context)
        

    
    return JsonResponse(context)


@should_be_marketer()
def marketer_add_agency(request):
    context = {}
    if request.method == "POST":
        response = {}
        id = request.user.id
        marketer = get_object_or_404(Marketer, id=id)
        
        agency_form = AddAgencyForm(data = request.POST)
        agency_email = agency_form["agency_email"].value()
        agency_mobile_no = agency_form["agency_mobile_no"].value()
        agency_whatsapp_mobile_no = agency_form["agency_whatsapp_mobile_no"].value()
        agency_gst_number = agency_form["agency_gst_number"].value()
        
        
        
        if validateUniqueAgencyEmail(agency_email) == False:
            response["result"] = False
            response["message"] = "EMAIL"
            return JsonResponse(response)

        if validateUniqueAgencyMbno(agency_mobile_no) == False:
            response["result"] = False       
            response["message"] = "MBNO"
            return JsonResponse(response)

        if validateUniqueAgencyWhatsAppMbno(agency_whatsapp_mobile_no) == False:
            response["result"] = False       
            response["message"] = "WS_MBNO"
            return JsonResponse(response)

        if validateUniqueAgencyGst(agency_gst_number) == False:
            response["result"] = False       
            response["message"] = "GST"
            return JsonResponse(response)

        if agency_form.is_valid():
            agency_obj = agency_form.save(commit=False)
            agency_obj.marketer_id = marketer
            agency_obj.save()

            response["message"] = "Agency has been successfully inserted"
            response["result"] = True
            return JsonResponse(response)
        else:
            response["result"] = False
            response["message"] = "Error in agency insertion!"
            response["errors"] = agency_form.errors
            return JsonResponse(response)
            



    agency_form = AddAgencyForm()
    context["agency_form"] = agency_form
    return render(request, "marketer/marketer_add_agency.html", context)


@should_be_marketer()
def marketer_add_ad(request):
    if request.method == "POST":
        pass
    else:
        id = request.user.id
        name = request.user.first_name
        marketer = get_object_or_404(Marketer, id=id)
        clients = Client.objects.filter(marketer_id=marketer)
        # ad_types = AdType.objects.filter(is_active = True)
        locations   =   Location.objects.filter(is_mah=False)
        mah_location   =   Location.objects.filter(is_mah=True)

        total_ads = Advt.objects.filter(order_id__marketer_id = marketer).count()
        form = AddAdForm()
        print(f"clients : {clients}")
        context = {
            'clients' : clients,
            # 'ad_types' : ad_types,
            "locations": locations,
            "mah_location": mah_location,
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
    q5 = Q(discount_requested = False)
    q6 = Q(gst_relax_requested = False)

    # order = Order.objects.filter(client_id = client).filter(marketer_id=marketer).filter(bill_status = False)
    order = Order.objects.filter(Q(q1) & Q(q2) & Q(q3) & Q(q4) & Q(q5) & Q(q6))
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





# import traceback

# @should_be_marketer()
# def marketer_save_ad2(request):
#     response = {}
#     print(request.POST)
#     post_data = request.POST
#     images = request.FILES
#     client_id = post_data.get("client")


#     id = request.user.id
#     marketer = get_object_or_404(Marketer, id=id)

#     client = get_object_or_404(Client, id=client_id)

#     ad_type_id = post_data.get("type")
#     ad_datetime = post_data.get("ad-datetime")
#     order_id = post_data.get("order_id")

#     print(request.POST)
    

#     order = get_object_or_404(Order, order_id=order_id)

#     ad_rate = AdType.objects.get(id = ad_type_id).rate

#     try:

#         frm = AddAdForm(data = request.POST, files = request.FILES)
#         adx = frm.save(commit = False)
#         adx.order_id = order

#         order.total_bill_amt += ad_rate
#         print(ad_rate)
#         order.save()
#         adx.ad_pub_date = ad_datetime
#         adx.client_id = client
#         adx.marketer_id = marketer
#         adx.save()
#     except Exception as e:
#         response['result'] = False
#         response['msg'] = f"Error in Ad Insertion : {e}"
#         return JsonResponse(response)
#     response['result'] = True
#     response['msg'] = "Ad Inserted"
#     totalAds = Advt.objects.filter(order_id=order).count()
#     response['totalAds'] = totalAds
#     return JsonResponse(response)

    
# Final version's (maybe) Ajax
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
    
    
    
    # ad_pub_dates = post_data.getlist("ad-datetime")

    
    ad_pub_dates = post_data.getlist("dateAndTimePicker1")
    print(f"Slots : {ad_pub_dates}")
    if len(ad_pub_dates) > 1:
        l1 = []
        for date in ad_pub_dates:
            if date not in l1:
                l1.append(date)
            else:
                # Duplicate slot found in current selected slots
                if date != "":
                    response["msg"] = f"Duplicate Slot : {date}"
                    response["result"] = False
                    return JsonResponse(response)

    pub_dates_obj = []
    for pub in ad_pub_dates:
        print(f"Pub : {pub}")
        if pub == "":
            obj = None
        else:
            p_str       = pub.split(" ")
            d_str       = p_str[0].replace("/", "-")
            t_str       = p_str[1]
            final_str   = d_str + " " + t_str
            obj         = datetime.strptime(final_str, "%Y-%m-%d %H:%M")
        pub_dates_obj.append(obj)

    

    for tx in pub_dates_obj:
        if(Advt.objects.filter(ad_pub_date = tx).exclude(ad_pub_date = None).count() > 0):
            response["result"] = False
            response["msg"] = f"Slot is already booked with Ad Slot: {tx}"
            print(pub_dates_obj)
            return JsonResponse(response)
    


    # date = datetime.strptime("2022-06-01 07:10:00", "%Y-%m-%d %H:%M:%S")
    


    ad_show_times = post_data.get("selectAdShowTimes") # Aka Ad Quantity
    is_ad_for_full_mah = post_data.get("checkLocationMaha") # Is Ad for Full Mah
    if(is_ad_for_full_mah == "on"):
        is_ad_for_full_mah = True
        fmh_ad_type_id = post_data.get("full_mah_ad_type")
        fm_ad_type_obj = get_object_or_404(Type, id= fmh_ad_type_id)


        fmh_loc_obj = Location.objects.filter(is_mah=True).filter(type=fm_ad_type_obj).first()

    else:
        is_ad_for_full_mah = False
    
 


    


    # ad_type_id = post_data.get("type")

    # image1 = images.getlist('ad_image')
    # print(dir(request.FILES))

    locations = post_data.get("location_ids[]")

    print(locations)
    print(post_data)
    print("Exit")

    locations = locations.split(",")
    locations.sort()
    print(locations)

    location_objects = Location.objects.filter(id__in=locations)


    # Order.objects.annotate(num_advts=Count('advts')).filter(num_advts__gt=1)
    # [order for order in Order.objects.all() if order.advt_set.count() > 1]
    # Backup SAVER CODE
    
    pic = request.FILES.get("ad_image", None)
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

    # ad_rate = AdType.objects.get(id = ad_type_id).rate
    

    for i in range(int(ad_show_times)):

        test_date = pub_dates_obj[i]



        frm = AddAdForm(data = request.POST)
        adx = frm.save(commit = False)

        adx.order_id = order
        # order.total_bill_amt += 100

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
        try:
            adx.save()
        except IntegrityError as e:
            response["result"] = False
            response["msg"] = f"Error {e}"
            return JsonResponse(response)


        if is_ad_for_full_mah == True:
            pass
            ad_loc = AdLoc()
            order.total_bill_amt += fmh_loc_obj.rate
            order.save()

            adx.ad_amt += fmh_loc_obj.rate
            adx.save()

            ad_loc.location = fmh_loc_obj
            ad_loc.advt_id = adx
            ad_loc.save()


        else:
            # Ver 3 
            for i,loc in enumerate(locations):
                ad_loc = AdLoc()
                loc_obj = location_objects[i]

                order.total_bill_amt += loc_obj.rate
                order.save()

                adx.ad_amt += loc_obj.rate
                adx.save()

                ad_loc.location = loc_obj
                ad_loc.advt_id = adx
                ad_loc.save()
        # ad_rate = all_ad_types.get(types)

    # except:
    #     response["result"] = False
    #     response["msg"] = "Error in insertion of Advt"
    #     return JsonResponse({"response":response})

    
    # BUG caught it shows all the ads of that marketer rather than for specific order
    # total_ads = Advt.objects.filter(order_id__marketer_id = marketer).count()
    # FIX ...
    total_ads = Advt.objects.filter(order_id = order).count()

    # Set final_bill_amt to total_bill_amt till discount is decided or not...
    order.final_bill_amt = order.total_bill_amt
    final_amt = order.total_bill_amt
    # print("Final amt")
    # print(final_amt)
    order.gst_final_bill_amt = final_amt + ((final_amt * 18) / 100)

    order.save()


    response["result"] = True
    response["msg"] = "All the Ad(s) added to cart!"
    response["totalAds"] = total_ads

    
    return JsonResponse(response)

@should_be_marketer()
def marketer_view_cart(request, order_id):
    # Remove the _ at start
    order_id = order_id[1:]
    id = request.user.id
    marketer = get_object_or_404(Marketer, id=id)
    # Does this marketer have permission to access this order or not?



    order = get_object_or_404(Order, order_id=order_id)

    if(order.marketer_id != marketer):
        return HttpResponse('Unauthorized', status=401)
    


    ads_obj = Advt.objects.filter(order_id=order)

    if(order.order_status != Order.Status.FRESH):
        orderviewform   =   SaveOrderUpdateForm(instance = order)
    else:
        orderviewform = None

    ro_upload_form = UpdateRoForm(instance = order)

    context = {
        "totalAds": ads_obj.count(),
        "order":order,
        "ads_obj": ads_obj,
        "orderviewform": orderviewform,
        "ro_upload_form": ro_upload_form
    }
    if order.discount_decision == True:
        new_discounted_amt = order.total_bill_amt - order.discount_alloted_amt
        context["discounted_new_bill"] = new_discounted_amt   

    return render(request, "marketer/marketer_view_cart.html", context)

@should_be_marketer()
def marketer_request_discount(request):
    response = {}
    order_id = request.POST.get("order_id")
    discount_requested = request.POST.get("discount_requested")
    total_bill_amt = request.POST.get("total_bill_amt")


    if discount_requested == None or total_bill_amt == None or order_id == None:
        response["result"] = False
        response["msg"] = "Invalid Amount"
        return JsonResponse(response)
    
    

    if(int(discount_requested) > int(total_bill_amt)):
        # Discount Amt greater than actual price REJECT
        response["result"] = False
        response["msg"] = "Invalid Amount"
    else:
        order = get_object_or_404(Order, order_id=order_id)
        order.discount_requested = True
        order.discount_req_amt = int(discount_requested)
        order.save()
        response["result"] = True
        response["msg"] = "Discount request done!"
    
    return JsonResponse(response)


@should_be_marketer()
def marketer_request_gst_relax(request):
    order_id = request.POST.get("order_id")
    context = {}
    id = request.user.id
    marketer = get_object_or_404(Marketer, id=id)
    order = get_object_or_404(Order, order_id=order_id)

    if(marketer != order.marketer_id):
        raise PermissionDenied()
    
    order.gst_relax_requested = True
    order.save()
    context["msg"] = "GST relax request has been sent, please wait for 24-36 hours for Head Office to accept/reject it"
    context["result"] = True
    return JsonResponse(context)


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


    order.total_bill_amt -= advt.ad_amt
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

    order = get_object_or_404(Order, order_id=order_id)
    
    # print(f"MOPZZ : {Order.Mop.Pdc_Cheque}")
    # if mode_of_pay == Order.Mop.Pdc_Cheque:
    #     print("Ohhhhh")
    #     exit()



    if(order.discount_decision == True):
        if((order.total_bill_amt - order.discount_alloted_amt)== order.discounted_new_bill_amt):
            order.final_bill_amt = order.discounted_new_bill_amt
            print("Match")
        else:
            print("Not Match")
    else:
        final_bill_amt = order.total_bill_amt


    order.order_status = Order.Status.IN_REVIEW
    order.mode_of_pay = mode_of_pay
    print(f"MOP : {mode_of_pay}")
    print(f"MOP Object : {order.mode_of_pay}")

    

    # exit()
    if mode_of_pay != Order.Mop.CASH and mode_of_pay != Order.Mop.CHEQUE and mode_of_pay != Order.Mop.Pdc_Cheque:
        order.trans_id = trans_id
    
    order.save()

    if order.client_id.agency_id != None:
        # Order is of agency
        order.agency_discount_given = True

        if order.gst_relax_decision == True:
            # No Gst Order
            order.b4_agency_discount_bill = order.final_bill_amt
            final_amt = order.final_bill_amt
            
        else:
            # Yes Gst Order
            order.b4_agency_discount_bill = order.gst_final_bill_amt
            final_amt = order.gst_final_bill_amt
        
        # If GST is applied final_amt will be GST amount otherwise normal amount

        
        if mode_of_pay == Order.Mop.Pdc_Cheque:
            pass
            
            order.agency_discount_percent = 20
            agency_discounted_amt = (final_amt * (20 / 100))
            order.agency_discount_amt = agency_discounted_amt

            end_amt = final_amt - agency_discounted_amt
            order.final_bill_amt = end_amt

        else:
            
            order.agency_discount_percent = 25
            agency_discounted_amt = (final_amt * (25 / 100))
            order.agency_discount_amt = agency_discounted_amt

            end_amt = final_amt - agency_discounted_amt
            order.final_bill_amt = end_amt

    order.save()
    print(f"FINALLY {order.mode_of_pay}")
    response["result"] = True
    response["msg"] = "Order Saved! Now you Accountant will verify the payment status & notify you"
    
    return JsonResponse(response)




def formatINR(number):
    s, *d = str(number).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)   



from django.template.loader import get_template
import imgkit
import json
import base64


@should_be_marketer()
def generate_ro(request, order_id):
    print(request.get_host())
    print(f"Order ID : {order_id}")
    order = get_object_or_404(Order, order_id = order_id)
    print(f"Order OBj : {order}")
    client_name = order.client_id.name

    template = get_template ('marketer/demo.html')
    print(f"Total are : {order.advt_set.all()}")
    final_bill_amt = formatINR(order.final_bill_amt)

    if(order.discount_decision == True):
        template_context = {
            'order': order,
            "client_name": client_name,
            "final_bill_amt" : final_bill_amt,
            "discounted_amt": formatINR(order.discount_alloted_amt)
        }
    else:
        template_context = {
            'order': order,
            "client_name": client_name,
            "final_bill_amt" : final_bill_amt
        }

    if order.client_id.agency_id != None:
        template_context['b4_agency_discount_bill'] = formatINR(order.b4_agency_discount_bill)
        template_context['agency_discount_amt'] = formatINR(order.agency_discount_amt)

        
    
    template_context['total_bill_amt'] = formatINR(order.total_bill_amt)
    template_context['gst_final_bill_amt'] = formatINR(order.gst_final_bill_amt)

    # print(template_context)

    html = template.render (template_context)
   
    
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8"
    }

    # Request for RO to remote server...

    # print("Ok came till here...")
    url = "http://159.223.76.134/generate-ro/"
    res = requests.post(url, data = {'pdf_string': html})
    print("came till content...")
    resp_json = json.loads(res.content)
    base64_data = resp_json['response']
    

    print(f"Response b64 size : {len(base64_data)}")

    xxx = base64.b64decode(base64_data)
    

    dump = HttpResponse(xxx, content_type='application/pdf')
    dump['Content-Disposition'] = 'attachment;filename="Release-Order.pdf"'
    return dump

    # exit()






    # Try converting HttpResponse object to bytes to string, now testing it in above snippet
    # html = "<h1>Hello Test COde </h1>"
    pdf = pdfkit.from_string(html, False, options)

    # response = HttpResponse(pdf, content_type='application/pdf')
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="Release-Order.pdf"'
    # return response

    # print("Start Response")
    # print(type(response))
    # print(dir(response))
    
    # print("End Response")
    # test = {}
    bin_data = response.serialize()
    base64_data = base64.b64encode(bin_data).decode('utf-8')
    

    # print("BASE 64 START")
    print("SOmethign...")
    print(type(base64_data))
    print(base64_data)
    yyy = base64.b64decode(base64_data)
    print(type(yyy))
    print(yyy)
    dx = HttpResponse(yyy, content_type='application/pdf')
    dx['Content-Disposition'] = 'attachment;filename="Release-Order.pdf"'

    return dx

    exit()
    # print("BASE 64 END")

    # print(f"b64 size : {len(base64_data)}")

    xxx = base64.b64decode(base64_data)
    
    # test = {}
    # test["response"] = str(xxx)
    # return JsonResponse(test)

    dump = HttpResponse(xxx, content_type='application/pdf')
    dump['Content-Disposition'] = 'attachment;filename="Release-Order.pdf"'

    return dump



    # html = '''
    # <h1>Hello OTT from Django</h1>
    # <i>Hello test</i>
    # '''
    # pdf = pdfkit.from_string(html, False)
    # response = HttpResponse(pdf,content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="release-order.pdf"'

    # return response

@should_be_marketer()
def request_release_order(request, order_id):
    response = {}
    print("Requesting release order to remote server....")
    response["msg"] = "Requesting release order to remote server...."
    return JsonResponse(response)


def test_ajax(request):
    print("Okkkkkkkkkkk")
    


@should_be_marketer()
def marketer_edit_ads(request):
    id = request.user.id
    marketer = get_object_or_404(Marketer, id=id)
    approved_unsigned_orders = Order.objects.filter(bill_status=True).filter(signed_release_order="").filter(marketer_id =marketer)
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
            print(marketer)
            print(f"All orders : {orders}")


    orders = [order for order in orders if order.advt_set.count() >= 1]
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
    id = request.user.id
    marketer = get_object_or_404(Marketer, id=id)
    advt = get_object_or_404(Advt, id=ad_id)
    if marketer != advt.order_id.marketer_id:
        # Seems tricky... this marketer has not bought this ad.. still
        # wanna view this advt... 
        # let's teach him/her a lesson
        raise PermissionDenied()

    if advt.is_published == True:
        raise PermissionDenied()

    
    if request.method == "POST":
        response = {}
        new_date_time = request.POST.get("dateAndTimePicker1")

        if new_date_time != "":
            new_pub_date_obj = []
            p_str       = new_date_time.split(" ")
            d_str       = p_str[0].replace("/", "-")
            t_str       = p_str[1]
            final_str   = d_str + " " + t_str
            obj         = datetime.strptime(final_str, "%Y-%m-%d %H:%M")
            if(Advt.objects.filter(ad_pub_date = obj).exclude(ad_pub_date = None).count() > 0):
                response["result"] = False
                response["message"] = f"Slot is already booked with Ad Slot: {obj}"
                return JsonResponse(response)
            

        form = UpdateAdForm(instance = advt, data = request.POST, files = request.FILES)
        if form.is_valid():
            if new_date_time == "":
                form.save()
                response["result"] = True
                response["message"] = "Advt is Updated"
                return JsonResponse(response)
            else:
                ad_obj = form.save(commit = False)
                ad_obj.ad_pub_date = obj
                ad_obj.save()
                response["result"] = True
                response["message"] = "Advt is Updated"
                return JsonResponse(response)

        else:
            response["result"] = False
            response["message"] = "Problem is Advt Updatation..."
            return JsonResponse(response)

    else:
        form = UpdateAdForm(instance = advt)
    context["advt"] = advt
    context["form"] = form
    
    return render(request, "marketer/marketer_edit_ad.html", context)



@should_be_marketer()
def marketer_manage_ro(request):
    approved_unsigned_orders = Order.objects.filter(bill_status=True).filter(signed_release_order="")
    print(approved_unsigned_orders)
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
    if(order.order_status != Order.Status.FRESH):
        orderviewform   =   SaveOrderUpdateForm(instance = order)
        ro_upload_form = UpdateRoForm(instance = order)
    else:
        orderviewform = None
        ro_upload_form = UpdateRoForm(instance = order)
    form = UpdateRoForm(instance = order)
    ads_obj = Advt.objects.filter(order_id=order)
    context = {
        "order": order,
        "orderviewform": orderviewform,
        "form": form,
        "totalAds": ads_obj.count(),
        "ro_upload_form": ro_upload_form,
    }
    if order.discount_decision == True:
        new_discounted_amt = order.total_bill_amt - order.discount_alloted_amt
        context["discounted_new_bill"] = new_discounted_amt   

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
    
