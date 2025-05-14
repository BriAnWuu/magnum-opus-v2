import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Auction


class AuctionConsumer(AsyncWebsocketConsumer):
    pass
