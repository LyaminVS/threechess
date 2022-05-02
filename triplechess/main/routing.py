from django.conf.urls import url
from .consumers import Chess

websocket_urlpatterns = [
    url(r'^ws/board/(?P<room_code>\w+)/$', Chess.as_asgi()),
]