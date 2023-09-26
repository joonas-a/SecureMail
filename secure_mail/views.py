from django.http import HttpResponseRedirect
from django.contrib import messages as notification
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from secure_mail.models import Message, User
# Create your views here.


@login_required
def index(request):
    print("User is authenticated: ", request.user.is_authenticated)
    return render(request, 'index.html')


def messages(request, username):
    data = Message.objects.filter(receiver=username)
    context = {"messages": data, "username": username}
    return render(request, 'messages.html', context)


@login_required
def newMessage(request):
    return render(request, 'messageForm.html')


@csrf_exempt
def create(request):
    recipient, content = (request.POST['recipient'], request.POST['content'])
    receiver = User.objects.filter(username=recipient)

    if not recipient.strip() or not content.strip():
        notification.error(
            request, message="Recipient and/or content was empty, and the data was not submitted.")
    elif not receiver:
        notification.error(
            request, message="Recipient was not found in the system, and the data was not submitted.")
    else:
        newMsg = Message.objects.create(
            sender=request.user, receiver=recipient, content=content)
        newMsg.save()
        notification.success(
            request, message=f"Your message to {recipient} was sent successfully!")
    # Use HttpResponseRedirect to avoid submitting data twice on page reload
    return HttpResponseRedirect("/")


def logout(request):
    logout(request)
    return redirect("/login")
