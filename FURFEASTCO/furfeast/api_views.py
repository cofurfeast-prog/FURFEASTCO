from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import CustomerMessage, Notification
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@login_required
@require_http_methods(["GET"])
def get_chat_messages(request, customer_id=None):
    """WhatsApp-style: Fetch last 100 messages from database"""
    from .models import ChatRoom
    try:
        if request.user.is_staff and customer_id:
            chat_room = ChatRoom.objects.get(customer_id=customer_id)
        else:
            chat_room, _ = ChatRoom.objects.get_or_create(customer=request.user)
        
        messages = chat_room.messages.order_by('created_at')[:100]
        
        data = [{
            'id': msg.id,
            'message': msg.message,
            'image': msg.image.url if msg.image else None,
            'is_from_admin': msg.is_from_admin,
            'is_read': msg.is_read,
            'created_at': msg.created_at.isoformat()
        } for msg in messages]
        
        return JsonResponse(data, safe=False)
    except ChatRoom.DoesNotExist:
        return JsonResponse([], safe=False)

@login_required
@require_http_methods(["POST"])
def api_send_customer_message(request):
    """Save customer message to database"""
    from .models import ChatRoom
    message_text = request.POST.get('message', '').strip()
    image = request.FILES.get('image')
    
    print(f"[DEBUG] api_send_customer_message called by {request.user.username}")
    print(f"[DEBUG] Message text: {message_text}")
    print(f"[DEBUG] Has image: {bool(image)}")
    
    if not message_text and not image:
        return JsonResponse({'success': False, 'error': 'Message or image required'}, status=400)
    
    chat_room, created = ChatRoom.objects.get_or_create(customer=request.user)
    print(f"[DEBUG] ChatRoom: {chat_room.id}, Created: {created}")
    
    msg = CustomerMessage.objects.create(
        chat_room=chat_room,
        message=message_text,
        image=image,
        is_from_admin=False
    )
    print(f"[DEBUG] Message created: ID={msg.id}, ChatRoom={msg.chat_room_id}")
    print(f"[DEBUG] Total messages in room: {chat_room.messages.count()}")
    
    return JsonResponse({
        'success': True,
        'message': {
            'id': msg.id,
            'message': msg.message,
            'image': msg.image.url if msg.image else None,
            'is_from_admin': False,
            'created_at': msg.created_at.isoformat()
        }
    })

@login_required
@require_http_methods(["POST"])
def api_send_admin_message(request):
    """Save admin message to database"""
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    message_text = request.POST.get('message', '').strip()
    image = request.FILES.get('image')
    user_id = request.POST.get('user_id')
    
    if not message_text and not image:
        return JsonResponse({'success': False, 'error': 'Message or image required'}, status=400)
    
    if not user_id:
        return JsonResponse({'success': False, 'error': 'Customer ID required'}, status=400)
    
    try:
        customer = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Customer not found'}, status=404)
    
    from .models import ChatRoom
    chat_room, _ = ChatRoom.objects.get_or_create(customer=customer)
    msg = CustomerMessage.objects.create(
        chat_room=chat_room,
        message=message_text,
        image=image,
        is_from_admin=True,
        is_read=False
    )
    
    # Broadcast via WebSocket to customer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"chat_{user_id}",
        {
            'type': 'chat_message',
            'message': msg.message,
            'image': msg.image.url if msg.image else None,
            'message_id': msg.id,
            'is_from_admin': True,
            'created_at': msg.created_at.isoformat()
        }
    )
    
    # Count unread messages from admin
    unread_count = chat_room.messages.filter(
        is_from_admin=True,
        is_read=False
    ).count()
    
    # Delete existing message notifications before creating new one
    Notification.objects.filter(
        user=customer,
        notification_type='message'
    ).delete()
    
    # Create single notification with total unread count
    if unread_count > 0:
        Notification.objects.create(
            user=customer,
            title=f' ({unread_count}) New Message from Seller',
            message='',
            link='/chat/',
            notification_type='message'
        )
    
    return JsonResponse({
        'success': True,
        'message': {
            'id': msg.id,
            'message': msg.message,
            'image': msg.image.url if msg.image else None,
            'is_from_admin': True,
            'is_read': False,
            'created_at': msg.created_at.isoformat()
        }
    })
