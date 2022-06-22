from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from user_admin.models import Post, Marketer, Client, AdType, Advt, Order

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from django.contrib import messages

from .decorators import should_be_marketer
from .forms import AddClientForm, AddAdForm

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
    return render(request, "marketer/marketer_home.html")



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
        marketer = get_object_or_404(Marketer, id=id)
        clients = Client.objects.filter(marketer_id=marketer)
        ad_types = AdType.objects.filter(is_active = True)
        form = AddAdForm()
        context = {
            'clients' : clients,
            'ad_types' : ad_types,
            "form": form
        }
    return render(request, "marketer/marketer_add_ad.html", context)

import time

@should_be_marketer()
def marketer_save_ad(request):
    print("came here!!!!!!!!!!!!!!!!!!")
    # print(dir(request))
    # print(request.POST)
    # print(request.FILES)
    order = Order.objects.all().first()
    post_data = request.POST
    images = request.FILES
    customer = post_data.get("customer")
    ad_pub_dates = post_data.getlist("ad-datetime")
    ad_show_times = post_data.get("selectAdShowTimes")

    # image1 = images.getlist('ad_image')
    # print(dir(request.FILES))


    
    pic = request.FILES["ad_image"]
    first_time = True

    saved_image = None

    # Ver 1 
    for i in range(int(ad_show_times)):

        test_date = ad_pub_dates[i]
        print(test_date)

        frm = AddAdForm(data = request.POST)
        adx = frm.save(commit = False)
        adx.order_id = order
        adx.ad_pub_date = test_date
        # adx.ad_image = images.get('ad_image')
        if first_time:
            first_time = False
            adx.ad_image = pic
            saved_image = adx.ad_image
        else:
            adx.ad_image = saved_image
        adx.save()
        # print(f"Image : {adx.ad_image}")
    # print(adx.order_id)



    # Ver 2
    # formset = AddAdFormset(data = request.POST, files= request.FILES)
    # if formset.is_valid():
    #     print("Is Vlid")
    # else:
    #     print("NOT")


    # print(descriptions[0])
    # ad_type = AdType.objects.get(id = ad_types[0])

    # ad_obj = Advt(
    #             desc = descriptions[0],
    #             type        =   ad_type,
    #             ad_pub_date =   ad_pub_dates[0],
    #             ad_image    =   image1
    #             )
    # ad_obj.save()


    # print(ad_obj.save())
    # print("Ad must be saved...")

    

    # print(customer)
    # pass


