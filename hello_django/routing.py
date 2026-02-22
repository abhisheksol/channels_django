from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/simple/", ChatConsumer.as_asgi()),
]