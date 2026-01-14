from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def test_notification_api(request):
    """Simple test view to check notifications"""
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    
    return JsonResponse({
        'user': request.user.username,
        'notification_count': notifications.count(),
        'notifications': [{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'created_at': str(n.created_at)
        } for n in notifications[:5]]
    })