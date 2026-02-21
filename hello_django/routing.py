from django.urls import path
from .consumers import SimpleConsumer

websocket_urlpatterns = [
    path("ws/simple/", SimpleConsumer.as_asgi()),
]