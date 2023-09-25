from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from secure_mail.models import Message
# Create your views here.

mockdata = ["asdkjjksdf", "asdffksldj", "lkl,mnsfkjd", "lkvcxjkldf"]


@login_required
def index(request):
    print("User is authenticated: ", request.user.is_authenticated)
    return render(request, 'index.html')


def messages(request, username):
    data = Message.objects.filter(receiver=username)
    context = {"messages": data, "username": username}
    return render(request, 'messages.html', context)


def logout(request):
    logout(request)
    return redirect("/login")
