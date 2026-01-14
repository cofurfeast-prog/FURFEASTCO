from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Product, ProductImage, FlashSale, PromoCode, Review, Cart, CartItem, Wishlist, Order, OrderItem, Notification

# User Admin - Ensure admin users are visible
admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')

# Core Models Admin

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        is_out_of_stock = cleaned_data.get('is_out_of_stock')
        stock = cleaned_data.get('stock')
        
        if is_out_of_stock and stock and stock > 0:
            raise ValidationError('Cannot mark item as out of stock when stock quantity is greater than 0.')
        
        return cleaned_data

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'category', 'price', 'original_price', 'stock', 'is_out_of_stock', 'is_bestseller', 'rating', 'updated_at')
    list_filter = ('category', 'is_out_of_stock', 'is_bestseller', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    
    class Media:
        js = ('js/admin_validation.js',)
        css = {
            'all': ('css/admin_custom.css',)
        }

# Marketing Models Admin

@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active', 'start_time', 'end_time')

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_amount', 'valid_from', 'valid_to', 'active')
    list_filter = ('active', 'valid_from', 'valid_to')

# User Interaction Models Admin

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_id', 'created_at', 'updated_at')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')

# Order Models Admin

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'user__username', 'user__email')
    readonly_fields = ('order_id', 'paypal_payment_id', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    def has_delete_permission(self, request, obj=None):
        return False  # Prevent accidental order deletion

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at',)
