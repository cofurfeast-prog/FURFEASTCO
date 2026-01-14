from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from furfeast.models import CustomerMessage

@login_required
def test_chat_messages(request):
    """Test endpoint to see all messages and API response"""
    user = request.user
    after_id = request.GET.get('after', 0)
    
    # Get all messages for user
    all_messages = CustomerMessage.objects.filter(user=user).order_by('created_at')
    
    # Get messages after specific ID
    new_messages = CustomerMessage.objects.filter(
        user=user,
        id__gt=after_id
    ).order_by('created_at')
    
    return JsonResponse({
        'user': user.username,
        'after_id': after_id,
        'total_messages': all_messages.count(),
        'new_messages_count': new_messages.count(),
        'all_messages': [{
            'id': msg.id,
            'message': msg.message,
            'is_from_admin': msg.is_from_admin,
            'created_at': msg.created_at.isoformat()
        } for msg in all_messages],
        'new_messages': [{
            'id': msg.id,
            'message': msg.message,
            'is_from_admin': msg.is_from_admin,
            'created_at': msg.created_at.isoformat()
        } for msg in new_messages]
    })
