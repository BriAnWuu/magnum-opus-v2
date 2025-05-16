import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from .models import Auction


class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['pk']
        self.auction_group_name = f'auction_{self.auction_id}'

        # Join auction group
        await self.channel_layer.group_add(
            self.auction_group_name,
            self.channel_name
        )

        await self.accept()

        # Get initial data
        initial_data = await self.get_initial_data()
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'data': initial_data
        }))

    async def disconnect(self, close_code):
        # Leave auction group
        await self.channel_layer.group_discard(
            self.auction_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'bid':
            bid_data = text_data_json.get('bid')
            if bid_data:
                await self.handle_bid(bid_data)

    async def send_bid_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'bid_update',
            'bid': event['bid']
        }))

    @database_sync_to_async
    def get_initial_data(self):
        try:
            auction = Auction.objects.get(pk=self.auction_id)
            return {
                'id': auction.pk,
                'seller': auction.seller,
                'title': auction.title,
                'description': auction.description,
                'image_url': auction.image_url,
                'starting_price': auction.starting_price,
                'current_bid': auction.current_bid,
                'end_time': auction.end_time.isoformat(),
                'created_at': auction.created_at.isoformat(),
                'updated_at': auction.updated_at.isoformat(),
                'is_active': auction.is_active
            }
        except Auction.DoesNotExist:
            return None

    @database_sync_to_async
    def handle_bid(self, bid_data):
        """
        Handle a bid received from the websocket.
        """
        try:
            auction = Auction.objects.get(pk=self.auction_id)
            # Validate bid

            new_price = float(bid_data['amount'])
            auction.current_bid = new_price
            auction.save()

            channel_layer = get_channel_layer()
            # Send bid update to auction group

        except Auction.DoesNotExist:
            print(f"Auction with id {self.auction_id} does not exist.")
            pass
