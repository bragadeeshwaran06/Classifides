# your_app_name/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ads.models import Message

class AdChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ad_id = self.scope['url_route']['kwargs']['ad_id']
        self.room_group_name = f'chat_{self.ad_id}'
        self.user = self.scope['user']

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.user
        ad_id = self.ad_id

        # Save message to database
        message_obj = Message.objects.create(
            sender=sender,
            ad_id=ad_id,
            content=message
        )

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
