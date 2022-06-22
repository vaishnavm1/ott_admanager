from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import *
from .models import Post


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

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
            print("Form invalid")
            messages.add_message(request, messages.ERROR, "Invalid username/password")
            return redirect("user_admin_login")
    else:
        context["form"] = form
        return render(request, "user_admin/user_admin_login.html", context)



@should_be_user_admin()
def user_admin_home(request):
    return render(request, "user_admin/user_admin_home.html")


@should_be_user_admin()
def user_admin_logout(request):
    logout(request)
    return redirect("user_admin_login")



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