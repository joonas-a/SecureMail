from django.urls import path

from .views import index, messages, newMessage, create

urlpatterns = [
    path("", index, name="index"),
    path("messages/<str:username>/", messages, name="messages"),
    path("new/", newMessage, name="new"),
    path("create/", create, name="create")
]
