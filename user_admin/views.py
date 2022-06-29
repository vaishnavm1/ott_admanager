from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import *
from .models import Post, Marketer, Order
from django.template.loader import render_to_string


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from datetime import datetime, timedelta

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
    context = {
        "marketers": marketers,
        "clients": clients
    }
    return render(request, "user_admin/user_admin_home.html", context)


@should_be_user_admin()
def user_admin_logout(request):
    logout(request)
    return redirect("user_admin_login")

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

    context["orders"] = queryset_orders
    html = render_to_string("user_admin/view_orders.html", context, request=request)

    return JsonResponse({"html": html})

@should_be_user_admin()
def search_marketers_clients(request):
    context = {}
    marketer_id = request.POST.get("m_id")
    marketer = get_object_or_404(Marketer, id=marketer_id)
    queryset = Client.objects.filter(marketer_id=marketer)
    context["talukas"] = queryset
    html = render_to_string("user_admin/tagify_clients.html", context, request=request)
    return JsonResponse({"form":html,"clients": list(queryset.values())})

# Old
# def user_admin_home(request):
#     print("1st line in home()")
#     if request.method == 'POST':
#         result = {}
#         print("POST Request came in")
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             result["result"] = True
#             return JsonResponse({"result":result})
#             # return HttpResponse("Post Uploaded Successfully!")
#         else:
#             result["result"] = False
#             # print(form.errors)
#             return JsonResponse({"result": result})

#     else:
#         print("Get Request in home()")
#         form = PostForm()
#     return render(request, 'user_admin/user_admin_home.html', {'form' : form})
  
  

def view_posts(request):
    posts = Post.objects.all()
    print(len(posts))
    context = {
        "posts":posts
    }
    return render(request, "user_admin/view-posts.html", context)