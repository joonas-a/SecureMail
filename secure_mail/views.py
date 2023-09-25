from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template import loader
# Create your views here.


@login_required
def index(request):
    print("User is authenticated: ", request.user.is_authenticated)
    return render(request, 'index.html')


def logout(request):
    logout(request)
    return redirect("/login")
