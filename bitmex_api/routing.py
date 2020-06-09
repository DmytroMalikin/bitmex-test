from django.urls import path
from bitmex_api import consumers

websocket_urlpatterns = [
    path('ws/bitmex_api/<uri>/', consumers.BitmexConsumer),
]
