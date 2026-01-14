from .models import PromoCode
from django.utils import timezone
from django.conf import settings

def promo_context(request):
    try:
        promo = PromoCode.objects.filter(
            active=True,
            valid_from__lte=timezone.now(),
            valid_to__gte=timezone.now()
        ).order_by('-valid_from').first()
    except Exception:
        promo = None
    
    # Get cart and wishlist counts from session
    cart_count = len(request.session.get('cart', []))
    wishlist_count = len(request.session.get('wishlist', []))
    
    return {
        'header_promo': promo,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'PAYPAL_CLIENT_ID': getattr(settings, 'PAYPAL_CLIENT_ID', '')
    }
