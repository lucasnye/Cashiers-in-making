from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/live_stt/$', consumers.LiveSTTConsumer.as_asgi()),
    re_path(r'^ws/dyslexia_format/$', consumers.DyslexiaPDFWebSocketConsumer.as_asgi()),
]
