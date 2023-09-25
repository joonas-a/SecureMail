from django.urls import path

from .views import index, messages

urlpatterns = [
    path("", index, name="index"),
    path("messages/<str:username>/", messages, name="messages"),
]
