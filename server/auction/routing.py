from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r'ws/auction/(?P<pk>\d+)/$',
        consumers.AuctionConsumer.as_asgi()
    ),
]
