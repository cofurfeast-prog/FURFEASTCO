import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.is_admin = self.user.is_staff
        self.room_name = f"chat_{self.user.id}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        
        query_string = self.scope.get('query_string', b'').decode()
        if 'customer_id=' in query_string and self.is_admin:
            customer_id = query_string.split('customer_id=')[1].split('&')[0]
            self.customer_room = f"chat_{customer_id}"
            await self.channel_layer.group_add(self.customer_room, self.channel_name)
            # Add admin to their own admin room for persistent message viewing
            self.admin_room = f"admin_chat_{self.user.id}"
            await self.channel_layer.group_add(self.admin_room, self.channel_name)
        
        await self.accept()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'room_name'):
            await self.channel_layer.group_discard(self.room_name, self.channel_name)
        if hasattr(self, 'customer_room'):
            await self.channel_layer.group_discard(self.customer_room, self.channel_name)
        if hasattr(self, 'admin_room'):
            await self.channel_layer.group_discard(self.admin_room, self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'notification')
        
        if message_type == 'typing':
            typing = data.get('typing', False)
            user_id = data.get('user_id')
            typing_data = {
                'type': 'typing_indicator',
                'is_typing': typing,
                'user_id': self.user.id,
                'is_admin': self.is_admin
            }
            if user_id and self.is_admin:
                await self.channel_layer.group_send(f"chat_{user_id}", typing_data)
            else:
                await self.channel_layer.group_send(self.room_name, typing_data)
        
        elif message_type == 'message':
            # Send full message data for instant rendering
            message_data = {
                'type': 'chat_message',
                'message': data.get('message'),
                'image': data.get('image'),
                'message_id': data.get('message_id'),
                'is_from_admin': self.is_admin,
                'created_at': data.get('created_at')
            }
            
            if self.is_admin:
                user_id = data.get('user_id')
                # Send to customer's room (admin is already listening there)
                await self.channel_layer.group_send(f"chat_{user_id}", message_data)
            else:
                # Send to customer's room (where admin is listening)
                await self.channel_layer.group_send(self.room_name, message_data)
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'image': event.get('image'),
            'message_id': event['message_id'],
            'is_from_admin': event['is_from_admin'],
            'created_at': event['created_at']
        }))
    
    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'typing': event['is_typing'],
            'is_admin': event.get('is_admin', False)
        }))
