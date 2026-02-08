from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Core Models

class PendingRegistration(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    password_hash = models.CharField(max_length=128)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Pending: {self.email}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, default='Nepal')
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_expires = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Delete old profile picture when uploading new one
        if self.pk:
            try:
                old_profile = UserProfile.objects.get(pk=self.pk)
                if old_profile.profile_picture and old_profile.profile_picture != self.profile_picture:
                    old_profile.profile_picture.delete(save=False)
            except UserProfile.DoesNotExist:
                pass
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('dog-food', 'Dog Food'),
        ('cat-food', 'Cat Food'),
        ('accessories', 'Accessories'),
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='dog-food', db_index=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original price (will show as strikethrough)")
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField(default=0)
    is_out_of_stock = models.BooleanField(default=False, db_index=True)
    is_bestseller = models.BooleanField(default=False, db_index=True)
    rating = models.FloatField(default=0.0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['category', 'is_out_of_stock']),
            models.Index(fields=['is_bestseller', 'is_out_of_stock']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['price']),
            models.Index(fields=['rating', 'is_out_of_stock']),
            models.Index(fields=['name']),  # For search queries
        ]
        ordering = ['-created_at']  # Default ordering

    def clean(self):
        from django.core.exceptions import ValidationError
        # Prevent saving if manually marked out of stock but has stock quantity
        if self.is_out_of_stock and self.stock > 0:
            raise ValidationError({
                'is_out_of_stock': 'Cannot mark item as out of stock when stock quantity is greater than 0.',
                'stock': 'Stock quantity must be 0 when item is marked as out of stock.'
            })
    
    def save(self, *args, **kwargs):
        # Delete old product image when uploading new one
        if self.pk:
            try:
                old_product = Product.objects.get(pk=self.pk)
                if old_product.image and old_product.image != self.image:
                    old_product.image.delete(save=False)
            except Product.DoesNotExist:
                pass
        
        # Run validation before saving
        self.full_clean()
        # Auto-set out of stock based on stock quantity only if not manually set
        if not self.is_out_of_stock:
            self.is_out_of_stock = (self.stock == 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Image for {self.product.name}"

# Marketing Models

class FlashSale(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=50, choices=Product.CATEGORY_CHOICES, null=True, blank=True, help_text="Category for flash sale (optional)")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    discount_percentage = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.category:
            return f"{self.discount_percentage}% OFF on {self.get_category_display()}"
        elif self.product:
            return f"{self.discount_percentage}% OFF on {self.product.name}"
        return f"{self.title or 'Flash Sale'} ({self.discount_percentage}% OFF)"

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Fixed discount amount")
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=50.00, help_text="Minimum order for free shipping")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

# User Interaction Models

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username if self.user else 'Guest ' + str(self.session_id)}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/')
    image_position_x = models.FloatField(default=50.0)
    image_position_y = models.FloatField(default=50.0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    writer_name = models.CharField(max_length=100, blank=True, help_text="Display name for the writer (optional, defaults to admin username)")
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_blog = Blog.objects.get(pk=self.pk)
                if old_blog.image and old_blog.image != self.image:
                    old_blog.image.delete(save=False)
            except Blog.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Order Models

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('paypal', 'PayPal'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    paypal_payment_id = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='paypal')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Shipping Information
    shipping_address = models.TextField(blank=True, null=True)
    shipping_phone = models.CharField(max_length=20, blank=True, null=True)
    shipping_city = models.CharField(max_length=100, blank=True, null=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    courier_name = models.CharField(max_length=50, blank=True, null=True, help_text="DHL, Pathao, Nepal Post, etc.")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Admin notes
    admin_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total_price(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# Content Management

class AboutUs(models.Model):
    title = models.CharField(max_length=200, default="About FurFeast")
    content = models.TextField()
    image = models.ImageField(upload_to='about/', null=True, blank=True)
    happy_pet_parents_count = models.CharField(max_length=20, default="10k+")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "About Us"
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_about = AboutUs.objects.get(pk=self.pk)
                if old_about.image and old_about.image != self.image:
                    old_about.image.delete(save=False)
            except AboutUs.DoesNotExist:
                pass
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class HeroImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='hero/', help_text="Legacy field - use desktop_image instead")
    desktop_image = models.ImageField(upload_to='hero/desktop/', null=True, blank=True, help_text="Landscape image for desktop (1920x800 recommended)")
    mobile_image = models.ImageField(upload_to='hero/mobile/', null=True, blank=True, help_text="Portrait/square image for mobile (800x800 recommended)")
    headline = models.CharField(max_length=200)
    subheadline = models.CharField(max_length=300)
    cta_text = models.CharField(max_length=50, default="Shop Now")
    cta_link = models.CharField(max_length=200, default="/shop/")
    align = models.CharField(max_length=10, choices=[('left', 'Left'), ('right', 'Right')], default='left')
    text_position_y = models.IntegerField(default=50, help_text="Text vertical position (0-100)")
    text_position_x = models.IntegerField(default=10, help_text="Text horizontal position (0-100)")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # If this is an update (not new), delete old images
        if self.pk:
            try:
                old_hero = HeroImage.objects.get(pk=self.pk)
                if old_hero.image and old_hero.image != self.image:
                    old_hero.image.delete(save=False)
                if old_hero.desktop_image and old_hero.desktop_image != self.desktop_image:
                    old_hero.desktop_image.delete(save=False)
                if old_hero.mobile_image and old_hero.mobile_image != self.mobile_image:
                    old_hero.mobile_image.delete(save=False)
            except HeroImage.DoesNotExist:
                pass
        
        # If adding new hero image and count will exceed 3, delete oldest
        if not self.pk:
            hero_count = HeroImage.objects.count()
            if hero_count >= 3:
                oldest = HeroImage.objects.order_by('created_at').first()
                if oldest:
                    oldest.delete()
        
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class MassEmailCampaign(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='campaigns/', null=True, blank=True)
    video = models.FileField(upload_to='campaigns/videos/', null=True, blank=True)
    sent_to_registered = models.BooleanField(default=False)
    sent_to_customers = models.BooleanField(default=False)
    sent_to_furfeast_family = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    recipients_count = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_campaign = MassEmailCampaign.objects.get(pk=self.pk)
                if old_campaign.image and old_campaign.image != self.image:
                    old_campaign.image.delete(save=False)
                if old_campaign.video and old_campaign.video != self.video:
                    old_campaign.video.delete(save=False)
            except MassEmailCampaign.DoesNotExist:
                pass
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.image and self.image.size > 5 * 1024 * 1024:  # 5MB
            raise ValidationError('Image size must be less than 5MB')
        if self.video and self.video.size > 50 * 1024 * 1024:  # 50MB
            raise ValidationError('Video size must be less than 50MB')

class BusinessTarget(models.Model):
    PERIOD_CHOICES = [
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('year', 'This Year'),
    ]
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField(default=2024)
    month = models.IntegerField(null=True, blank=True)
    week = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['period', 'year', 'month', 'week']
    
    def __str__(self):
        return f"{self.get_period_display()} Target: ${self.target_amount}"

class FurFeastFamily(models.Model):
    PET_CATEGORY_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=100)
    pet_category = models.CharField(max_length=20, choices=PET_CATEGORY_CHOICES)
    pet_age = models.CharField(max_length=50)
    favourite_food = models.CharField(max_length=200)
    additional_description = models.TextField(blank=True)
    receive_expert_emails = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.pet_name} ({self.get_pet_category_display()})"

class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    notification_type = models.CharField(max_length=50, default='general', choices=[('general', 'General'), ('message', 'Message'), ('order', 'Order')])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class ChatRoom(models.Model):
    """Chat room for customer-admin conversations"""
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chat_room')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Chat: {self.customer.username}"
    
    @property
    def has_unread_messages(self):
        return self.messages.filter(is_from_admin=True, is_read=False).exists()

class CustomerMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    message = models.TextField()
    image = models.ImageField(upload_to='chat/', null=True, blank=True)
    is_from_admin = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_message = CustomerMessage.objects.get(pk=self.pk)
                if old_message.image and old_message.image != self.image:
                    old_message.image.delete(save=False)
            except CustomerMessage.DoesNotExist:
                pass
        super().save(*args, **kwargs)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.image:
            if self.image.size > 1048576:
                raise ValidationError('Image size must be less than 1MB')
            import os
            ext = os.path.splitext(self.image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise ValidationError('Only JPEG and PNG images are allowed')
    
    def __str__(self):
        return f"{self.chat_room.customer.username} - {'Admin' if self.is_from_admin else 'Customer'} - {self.created_at}"

# Chatbot Models

class ChatBotIntent(models.Model):
    name = models.CharField(max_length=100, unique=True)
    keywords = models.JSONField(help_text="List of keywords that trigger this intent")
    response_template = models.TextField()
    priority = models.IntegerField(default=0, help_text="Higher priority intents are checked first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-priority', 'name']
    
    def __str__(self):
        return self.name

class ChatBotSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    context = models.JSONField(default=dict)
    last_intent = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"ChatBot Session: {self.user.username if self.user else self.session_id}"

class ChatBotConversation(models.Model):
    session = models.ForeignKey(ChatBotSession, on_delete=models.CASCADE, related_name='conversations')
    user_message = models.TextField()
    bot_response = models.TextField()
    intent_matched = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Chat: {self.user_message[:50]}..."