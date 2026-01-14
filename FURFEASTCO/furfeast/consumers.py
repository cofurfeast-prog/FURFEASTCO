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
        
        await self.accept()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'room_name'):
            await self.channel_layer.group_discard(self.room_name, self.channel_name)
        if hasattr(self, 'customer_room'):
            await self.channel_layer.group_discard(self.customer_room, self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        user_id = data.get('user_id')
        typing = data.get('typing', False)
        
        # Handle typing indicator
        if typing:
            typing_data = {
                'type': 'typing_indicator',
                'is_typing': True,
                'user_id': self.user.id,
                'is_admin': self.is_admin
            }
            if user_id and self.is_admin:
                await self.channel_layer.group_send(f"chat_{user_id}", typing_data)
            else:
                await self.channel_layer.group_send(self.room_name, typing_data)
            return
        
        if message:
            if user_id and self.is_admin:
                msg = await self.save_admin_message(user_id, message)
                msg_data = {
                    'type': 'chat_message',
                    'message': {
                        'id': msg.id,
                        'message': msg.message,
                        'is_from_admin': True,
                        'is_read': False,
                        'created_at': msg.created_at.isoformat()
                    }
                }
                await self.channel_layer.group_send(f"chat_{user_id}", msg_data)
            else:
                msg = await self.save_customer_message(message)
                msg_data = {
                    'type': 'chat_message',
                    'message': {
                        'id': msg.id,
                        'message': msg.message,
                        'is_from_admin': False,
                        'created_at': msg.created_at.isoformat()
                    }
                }
                await self.channel_layer.group_send(self.room_name, msg_data)
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))
    
    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'typing': event['is_typing'],
            'is_admin': event.get('is_admin', False)
        }))
    
    @database_sync_to_async
    def save_customer_message(self, message):
        from .models import CustomerMessage
        return CustomerMessage.objects.create(
            user=self.user,
            message=message,
            is_from_admin=False
        )
    
    @database_sync_to_async
    def save_admin_message(self, user_id, message):
        from .models import CustomerMessage, Notification
        user = User.objects.get(id=user_id)
        msg = CustomerMessage.objects.create(
            user=user,
            message=message,
            is_from_admin=True,
            is_read=False
        )
        # Create notification for customer
        Notification.objects.create(
            user=user,
            title='New Message from Seller',
            message=f'💬 {message[:50]}...' if len(message) > 50 else f'💬 {message}',
            link='/chat/',
            notification_type='message'
        )
        return msg
