# FurFeast Co. - Development Guidelines

## Code Quality Standards

### Import Organization
- **Standard Library First**: Python standard library imports at the top
- **Third-Party Next**: Django and external packages follow
- **Local Imports Last**: Project-specific imports at the end
- **Explicit Imports**: Import specific classes/functions rather than entire modules
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order
```

### Naming Conventions
- **Functions/Methods**: Snake_case with descriptive verbs (`get_context_data`, `add_to_cart`, `update_order_status`)
- **Classes**: PascalCase for models and classes (`UserProfile`, `CustomerMessage`, `FlashSale`)
- **Constants**: UPPERCASE with underscores (`STATUS_CHOICES`, `PAYMENT_METHOD_CHOICES`)
- **Template Variables**: Snake_case (`cart_count`, `wishlist_items`, `notification_badge`)
- **URL Names**: Snake_case with prefixes (`dashboard_home`, `dashboard_product_list`)

### Documentation Standards
- **Docstrings**: Triple-quoted strings for function/class documentation
- **Inline Comments**: Explain complex logic, not obvious code
- **Model Field Help Text**: Provide user-friendly descriptions for admin interface
```python
def get_context_data(request):
    """
    Returns common context data like cart_count and wishlist_count.
    Always fresh data - no caching for user-specific data.
    """
```

### Code Formatting
- **Indentation**: 4 spaces (no tabs)
- **Line Length**: Keep under 120 characters where practical
- **Blank Lines**: Two blank lines between top-level functions/classes
- **String Quotes**: Single quotes for strings, double quotes for user-facing text
- **F-strings**: Preferred for string formatting (`f'Order {order.order_id}'`)

## Django-Specific Patterns

### View Architecture

**Function-Based Views (FBVs)**
- Primary pattern used throughout the codebase
- Decorated with `@login_required` for authentication
- Use `@require_POST` for POST-only endpoints
- Use `@user_passes_test(is_admin)` for admin-only views
```python
@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Implementation
    return JsonResponse({'status': 'success'})
```

**View Decorators Pattern**
- `@never_cache`: For user-specific pages (cart, profile, notifications)
- `@cache_page(60 * 3)`: For semi-static content (shop listings)
- `@vary_on_headers('Cookie')`: Cache varies by user authentication
```python
@login_required
@never_cache
def cart_view(request):
    context = get_context_data(request)
    cart, created = Cart.objects.prefetch_related('items__product').get_or_create(user=request.user)
    response = render(request, 'furfeast/cart.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response
```

### Model Design Patterns

**Field Definitions**
- Use `choices` for fixed options (status, categories)
- Add `db_index=True` for frequently queried fields
- Use `help_text` for admin clarity
- Set appropriate `blank=True, null=True` for optional fields
```python
category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='dog-food', db_index=True)
tracking_number = models.CharField(max_length=100, blank=True, null=True)
```

**Model Methods and Properties**
- Use `@property` for computed values that don't require database queries
- Implement `__str__` for readable admin representations
- Override `save()` for custom logic (validation, file cleanup)
- Use `clean()` for model-level validation
```python
@property
def total_price(self):
    return sum(item.total_price for item in self.items.all())

def __str__(self):
    return f"Order {self.order_id} - {self.user.username}"
```

**Meta Options**
- Define `ordering` for default query order
- Use `indexes` for composite index optimization
- Set `unique_together` for multi-field uniqueness
```python
class Meta:
    ordering = ['-created_at']
    indexes = [
        models.Index(fields=['category', 'is_out_of_stock']),
        models.Index(fields=['-created_at']),
    ]
```

### Query Optimization

**Select Related / Prefetch Related**
- Use `select_related()` for ForeignKey and OneToOne relationships
- Use `prefetch_related()` for ManyToMany and reverse ForeignKey
- Chain optimizations for complex queries
```python
orders = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')
products = Product.objects.select_related()
chat_messages = CustomerMessage.objects.filter(user=customer).order_by('created_at')
```

**Efficient Counting and Aggregation**
- Use `Count()` and `Sum()` for aggregations
- Use `annotate()` for per-object calculations
- Filter with `Q` objects for complex conditions
```python
from django.db.models import Count, Sum, Q

customers = User.objects.filter(is_staff=False).annotate(
    total_orders=Count('order'),
    total_spent=Sum('order__total_amount')
)
```

**Pagination Pattern**
- Use Django's `Paginator` for large result sets
- Default to 12-20 items per page
```python
from django.core.paginator import Paginator

paginator = Paginator(products, 12)
page_obj = paginator.get_page(request.GET.get('page'))
```

### Form Handling

**POST Request Pattern**
- Check `request.method == 'POST'` for form submissions
- Use `request.POST.get()` with defaults for safe access
- Use `request.FILES.get()` for file uploads
- Validate and sanitize all user input
```python
if request.method == 'POST':
    name = request.POST.get('name')
    price = request.POST.get('price')
    image = request.FILES.get('image')
    is_bestseller = request.POST.get('is_bestseller') == 'on'
```

**JSON API Pattern**
- Use `json.loads(request.body)` for JSON payloads
- Return `JsonResponse` with consistent structure
- Include `success` boolean and descriptive messages
```python
try:
    data = json.loads(request.body)
    order_id = data.get('orderID')
    return JsonResponse({'success': True, 'message': 'Order created'})
except json.JSONDecodeError:
    return JsonResponse({'success': False, 'error': 'Invalid JSON'})
```

### Authentication and Authorization

**Login Required Pattern**
- Use `@login_required` decorator for authenticated views
- Check `request.user.is_authenticated` in templates
- Redirect to login page for unauthenticated users
```python
@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
```

**Admin Access Pattern**
- Define `is_admin(user)` helper function
- Use `@user_passes_test(is_admin)` decorator
- Check `user.is_staff` for admin privileges
```python
def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def dashboard_home(request):
    # Admin-only view
```

### Message Framework
- Use Django's messages framework for user feedback
- Standard levels: `success`, `error`, `warning`, `info`
- Messages persist across redirects
```python
from django.contrib import messages

messages.success(request, 'Product created successfully.')
messages.error(request, 'Invalid email or password.')
```

### File Upload Handling

**Image Processing**
- Validate file size and type before processing
- Use Pillow (PIL) for image manipulation
- Process to standard dimensions for consistency
- Delete old files when uploading new ones
```python
from PIL import Image as PILImage
from django.core.files.base import ContentFile
import io

def process_hero_image(image_file):
    img = PILImage.open(image_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    # Resize and crop logic
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=95, optimize=True)
    return ContentFile(output.getvalue())
```

**File Cleanup Pattern**
- Override model `save()` to delete old files
- Use `delete(save=False)` to remove file without saving model
```python
def save(self, *args, **kwargs):
    if self.pk:
        try:
            old_product = Product.objects.get(pk=self.pk)
            if old_product.image and old_product.image != self.image:
                old_product.image.delete(save=False)
        except Product.DoesNotExist:
            pass
    super().save(*args, **kwargs)
```

## Real-Time Features (Django Channels)

### WebSocket Consumer Pattern
- Use `AsyncWebsocketConsumer` for async operations
- Authenticate in `connect()` method
- Use channel layers for group messaging
- Handle both customer and admin connections
```python
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.room_name = f"chat_room_{self.user.id}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
```

### Notification System
- Create notifications on order status changes
- Use `notification_type` field for categorization ('order', 'message')
- Link notifications to related objects (orders)
- Mark as read when user views
```python
Notification.objects.create(
    user=order.user,
    title=f'Order {order.get_status_display()}',
    message=f'Your order #{order.order_id} has been shipped! 🚚',
    order=order,
    link=f'/order-tracking/{order.order_id}/',
    notification_type='order'
)
```

## Frontend JavaScript Patterns

### Component Architecture
- Store reusable components in `SHARED_COMPONENTS` object
- Use `innerHTML` for static template injection
- Use `createElement` and `appendChild` for dynamic content
- Separate concerns: layout injection vs. event handling

### Event Handling
- Use event delegation for dynamic elements
- Remove old listeners before adding new ones
- Use `{ passive: true }` for scroll/touch events
- Use `requestAnimationFrame` for DOM updates
```javascript
openBtn.addEventListener('click', openMenu, { passive: true });

requestAnimationFrame(() => {
    cartBadge.textContent = cartCount;
    cartBadge.classList.toggle('opacity-0', parseInt(cartCount) <= 0);
});
```

### AJAX Pattern
- Use `fetch()` API for async requests
- Include CSRF token from cookies for POST requests
- Add cache-busting timestamps for fresh data
- Handle errors gracefully with try-catch
```javascript
fetch(`/api/notifications/?t=${Date.now()}`, {
    cache: 'no-store',
    headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
})
.then(response => response.json())
.then(data => {
    // Handle response
})
.catch(error => console.error('Error:', error));
```

### DOM Manipulation Best Practices
- Cache DOM queries in variables
- Use `classList.toggle()` for conditional classes
- Clear content with `textContent = ''` before rebuilding
- Use `createElement` for security (avoid XSS)
```javascript
const notificationList = document.getElementById('notification-list');
notificationList.textContent = ''; // Clear existing

const notificationDiv = document.createElement('div');
notificationDiv.className = 'p-4 border-b';
notificationDiv.textContent = notification.message;
notificationList.appendChild(notificationDiv);
```

## Security Practices

### CSRF Protection
- Include CSRF token in all POST requests
- Use `@csrf_exempt` sparingly (only for external webhooks)
- Get token from cookies in JavaScript
```python
def getCookie(name):
    if document.cookie and document.cookie !== '':
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            if (cookie.trim().startsWith(name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    return null;
```

### Input Validation
- Validate all user input on server side
- Use `get_object_or_404()` for safe object retrieval
- Check permissions before allowing actions
- Sanitize file uploads (size, type, content)
```python
if image.size > 10 * 1024 * 1024:  # 10MB
    messages.error(request, 'Image file must be less than 10MB')
    return render(request, template, context)
```

### SQL Injection Prevention
- Use Django ORM (never raw SQL with user input)
- Use parameterized queries if raw SQL is necessary
- Filter with Q objects, not string concatenation

## Performance Optimization

### Caching Strategy
- Cache global data (promo codes, flash sales) for 15 minutes
- Never cache user-specific data (cart, wishlist, notifications)
- Use `cache.get()` and `cache.set()` for manual caching
- Set appropriate cache headers for responses
```python
promo = cache.get('header_promo')
if not promo:
    promo = PromoCode.objects.filter(active=True, valid_to__gt=now).first()
    cache.set('header_promo', promo, 900)  # 15 minutes
```

### Database Optimization
- Add indexes to frequently queried fields
- Use `select_related()` and `prefetch_related()` to reduce queries
- Avoid N+1 query problems
- Use `only()` and `defer()` for large models when appropriate

### Static File Optimization
- Use WhiteNoise for static file serving
- Enable compression with `CompressedManifestStaticFilesStorage`
- Set long cache times for static assets
- Use TailwindCSS JIT for minimal CSS bundle size

## Error Handling

### Try-Except Pattern
- Catch specific exceptions, not bare `except:`
- Log errors for debugging
- Return user-friendly error messages
- Use `finally` for cleanup operations
```python
try:
    order = Order.objects.create(...)
    return JsonResponse({'success': True, 'order_id': order.order_id})
except Cart.DoesNotExist:
    return JsonResponse({'success': False, 'error': 'Cart not found'})
except Exception as e:
    print(f"Error: {str(e)}")
    return JsonResponse({'success': False, 'error': 'Order processing failed'})
```

### Validation Pattern
- Use model `clean()` method for validation
- Raise `ValidationError` with descriptive messages
- Call `full_clean()` before saving if needed
```python
def clean(self):
    from django.core.exceptions import ValidationError
    if self.is_out_of_stock and self.stock > 0:
        raise ValidationError({
            'is_out_of_stock': 'Cannot mark as out of stock when stock > 0'
        })
```

## Testing Considerations

### Debug Endpoints
- Create test views for debugging (admin-only)
- Include health check endpoints
- Log important operations for troubleshooting
```python
def health_check(request):
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
```

## Environment Configuration

### Settings Pattern
- Use `python-dotenv` for environment variables
- Provide sensible defaults with `os.getenv('KEY', 'default')`
- Keep secrets in `.env` file (never commit)
- Use different settings for development vs. production
```python
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
```

### Storage Configuration
- Use custom storage backend (Supabase) for file uploads
- Configure via `STORAGES` setting (Django 4.2+)
- Separate static files (WhiteNoise) from media files (Supabase)
```python
STORAGES = {
    "default": {
        "BACKEND": "furfeast.storage.SupabaseStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

## Common Idioms

### Get or Create Pattern
```python
cart, created = Cart.objects.get_or_create(user=request.user)
profile, created = UserProfile.objects.get_or_create(user=user)
```

### Update or Create Pattern
```python
BusinessTarget.objects.update_or_create(
    period=period,
    year=now.year,
    defaults={'target_amount': amount}
)
```

### Bulk Operations
```python
# Mark multiple as read
CustomerMessage.objects.filter(user=customer, is_from_admin=False, is_read=False).update(is_read=True)

# Delete multiple
cart.items.all().delete()
```

### Conditional Filtering
```python
products = Product.objects.all()
if category_param:
    products = products.filter(category=category_param)
if min_price:
    products = products.filter(price__gte=float(min_price))
```

### Time-based Filtering
```python
from datetime import timedelta
from django.utils import timezone

now = timezone.now()
week_start = now - timedelta(days=now.weekday())
orders = Order.objects.filter(created_at__gte=week_start)
```
