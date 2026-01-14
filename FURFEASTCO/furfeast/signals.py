from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Order, Notification
from django.utils import timezone

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when a new User is created"""
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.get_or_create(user=instance)

# Store the old status before saving
@receiver(pre_save, sender=Order)
def store_old_order_status(sender, instance, **kwargs):
    """Store the old status before saving"""
    if instance.pk:
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Order.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    """Create notification when order status changes"""
    if not created and hasattr(instance, '_old_status'):
        old_status = instance._old_status
        
        # Check if status changed to shipped
        if instance.status == 'shipped' and old_status != 'shipped':
            # Update shipped_at timestamp
            if not instance.shipped_at:
                instance.shipped_at = timezone.now()
                instance.save(update_fields=['shipped_at'])
            
            # Create notification for customer
            Notification.objects.create(
                user=instance.user,
                title="Order Shipped!",
                message=f"Your order #{instance.order_id} has been shipped{' via ' + instance.courier_name if instance.courier_name else ''}. {('Tracking number: ' + instance.tracking_number) if instance.tracking_number else ''}",
                order=instance
            )
        
        # Check if status changed to delivered
        elif instance.status == 'delivered' and old_status != 'delivered':
            # Update delivered_at timestamp
            if not instance.delivered_at:
                instance.delivered_at = timezone.now()
                instance.save(update_fields=['delivered_at'])
            
            # Create notification for customer
            Notification.objects.create(
                user=instance.user,
                title="Order Delivered!",
                message=f"Your order #{instance.order_id} has been delivered successfully. Thank you for shopping with FurFeast!",
                order=instance
            )