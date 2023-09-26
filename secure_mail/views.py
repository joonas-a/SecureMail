from django.http import HttpResponseRedirect
from django.contrib import messages as notification
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from secure_mail.models import Message, User
from django.core.exceptions import PermissionDenied
import sqlite3
# Create your views here.


@login_required
def index(request):
    # print("User is authenticated: ", request.user.is_authenticated)
    return render(request, 'index.html')


"""
Flaw 1: Broken Access Control

Users are able to view their private messages while not logged in, by typing
the url by hand. e.g. alice's private messages with 'localhost:8000/messages/alice'

Fix: With Django the login status can be verified with @login_required decorator-function.
To fix the vulnerability, uncomment @login_required on row ADD_ROW_HERE

Flaw 4: Identification and Authentication Failures

After the previous fix, '/messages/*' will no longer be accessible unless logged in.
Still, the user is able to view other users private messages, by handtyping the url.
For example, view bob's messages while logged in as alice: 'localhost:8000/messages/bob'

Fix: Before loading the page, make sure the current user is privileged to see the page.
Django stores currently logged user details in the session.

"""

# Flaw 1
# @login_required
def messages(request, username):
    # Flaw 4
    # if username != request.user.username:
    #     raise PermissionDenied()
    data = Message.objects.filter(receiver=username)
    context = {"messages": data, "username": username}
    return render(request, 'messages.html', context)


@login_required
def newMessage(request):
    return render(request, 'messageForm.html')


"""
Flaw 5: CSRF-Vulnerability

Django has built in CSRF-protection, so in order for us to not have our form
protected, we have to explicitly declare the function to be csrf_exempt.

Fix: remove @csrf_exempt from below, and add
{% csrf_token %}-tag to the form in 'messageForm.html'

Flaw 2: SQL-injection

Action for sending new messages is using an insecure SQL-query, where user input
is not sanitized at all. If someone was to send a message to an existing user
(alice, bob or secure) with content:
'); DROP TABLE secure_mail_message; --
the app would no longer function at all, unless the whole db was rebuilt.

Fix: Use django's built in ORM for database actions, as can be seen commented below
the insecure query.
"""


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
        # Flaw 2:
        con = sqlite3.connect('db.sqlite3')
        cursor = con.cursor()
        cursor.executescript(
            f"INSERT INTO secure_mail_message (sender, receiver, content) VALUES ('{request.user.username}', '{receiver[0].username}', '{content}')")

        con.commit()
        con.close()
        # Fix for SQL-injection
        # newMsg = Message.objects.create(
        #     sender=request.user, receiver=recipient, content=content)
        # newMsg.save()
        notification.success(
            request, message=f"Your message to {recipient} was sent successfully!")
    # Use HttpResponseRedirect to avoid submitting data twice on page reload
    return HttpResponseRedirect("/")


def logout(request):
    logout(request)
    return redirect("/login")
