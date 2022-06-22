from django.shortcuts import render
from django.http import HttpResponse
from user_admin.models import Post

def front_home(request):
    return HttpResponse("Ok")

def front_test(request):
    posts = Post.objects.all()
    context = {
        "posts": posts
    }
    return render(request, "front/home.html", context)