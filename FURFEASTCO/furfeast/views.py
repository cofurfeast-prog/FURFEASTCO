from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.vary import vary_on_headers
from django.views.decorators.cache import never_cache
from django.db.models import Q, Prefetch, Avg
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from datetime import timedelta
import json
import uuid
from .models import Product, Cart, CartItem, Wishlist, Blog, FlashSale, PromoCode, UserProfile, Order, OrderItem, AboutUs, FurFeastFamily, PendingRegistration, Review, ContactMessage, Notification, CustomerMessage, ChatBotIntent, ChatBotSession, ChatBotConversation
from decimal import Decimal, InvalidOperation

# Health check view for debugging
def health_check(request):
    """Simple health check endpoint"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'debug': settings.DEBUG,
            'allowed_hosts': settings.ALLOWED_HOSTS
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)

# Helper Functions

def get_context_data(request):
    """
    Returns common context data like cart_count and wishlist_count.
    Always fresh data - no caching for user-specific data.
    """
    context = {
        'cart_count': 0,
        'wishlist_count': 0,
        'notification_count': 0,
    }
    
    try:
        if request.user.is_authenticated:
            # Always get fresh counts - no caching for user data
            cart, created = Cart.objects.get_or_create(user=request.user)
            context['cart_count'] = cart.items.count()
            context['wishlist_count'] = Wishlist.objects.filter(user=request.user).count()
            context['notification_count'] = Notification.objects.filter(user=request.user, is_read=False).count()
        
        # Only cache global promo code (not user-specific)
        promo = cache.get('header_promo')
        if not promo:
            now = timezone.now()
            promo = PromoCode.objects.filter(active=True, valid_to__gt=now).first()
            cache.set('header_promo', promo, 900)  # 15 minutes
        context['header_promo'] = promo
    except Exception as e:
        # Return basic context if database fails
        pass
        
    return context

# Views

def index(request):
    """Simple homepage that works without database"""
    context = {
        'cart_count': 0,
        'wishlist_count': 0,
        'notification_count': 0,
        'flash_sale': None,
        'promo_codes': [],
        'hero_images': [],
        'featured_products': [],
        'customer_reviews': [],
    }
    
    try:
        context = get_context_data(request)
        now = timezone.now()
        
        # Get fresh data - no caching
        context['flash_sale'] = FlashSale.objects.filter(is_active=True, end_time__gt=now).first()
        context['promo_codes'] = PromoCode.objects.filter(active=True, valid_to__gt=now)
        
        # Get hero images
        from .models import HeroImage
        context['hero_images'] = HeroImage.objects.filter(is_active=True).order_by('order')
        
        # Get featured products fresh
        bestsellers = list(Product.objects.filter(is_bestseller=True)[:4])
        if len(bestsellers) < 4:
            recent_products = list(Product.objects.exclude(id__in=[p.id for p in bestsellers]).order_by('-created_at')[:4-len(bestsellers)])
            featured_products = bestsellers + recent_products
        else:
            featured_products = bestsellers
        context['featured_products'] = featured_products
        
        # Get recent customer reviews (max 10, ordered by newest)
        context['customer_reviews'] = Review.objects.select_related('user', 'product').order_by('-created_at')[:10]
        
        return render(request, 'furfeast/index.html', context)
    except Exception as e:
        # For development - render template with empty context instead of error message
        return render(request, 'furfeast/index.html', context)

@vary_on_headers('Cookie')
@cache_page(60 * 3)  # Cache for 3 minutes, varies by user
def shop(request):
    return product_list(request)

def dog_food(request):
    return product_list(request, category_slug='dog-food')

def cat_food(request):
    return product_list(request, category_slug='cat-food')

def accessories(request):
    return product_list(request, category_slug='accessories')

def product_list(request, category_slug=None):
    context = get_context_data(request)
    
    # Optimize with select_related for better performance
    products = Product.objects.select_related()
    
    # Apply filters
    category_param = request.GET.get('category')
    if category_param:
        products = products.filter(category=category_param)
        context['category_slug'] = category_param
    elif category_slug:
        products = products.filter(category=category_slug)
        context['category_slug'] = category_slug
    
    # Rating filter
    rating_filter = request.GET.get('rating')
    if rating_filter:
        try:
            min_rating = float(rating_filter)
            products = products.filter(rating__gte=min_rating)
            context['rating_filter'] = rating_filter
        except ValueError:
            pass
    
    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
            context['min_price'] = min_price
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
            context['max_price'] = max_price
        except ValueError:
            pass
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else: # newest
        products = products.order_by('-created_at')
        
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)
    
    context.update({
        'products': page_obj,
        'sort_by': sort_by,
    })
    
    template_name = 'furfeast/shop.html'
    if category_slug:
        if category_slug == 'dog-food': template_name = 'furfeast/dog-food.html'
        elif category_slug == 'cat-food': template_name = 'furfeast/cat-food.html'
        elif category_slug == 'accessories': template_name = 'furfeast/accessories.html'
            
    return render(request, template_name, context)

@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is out of stock
    if product.is_out_of_stock or product.stock == 0:
        return JsonResponse({
            'status': 'error',
            'message': f'{product.name} is currently out of stock'
        })
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'quantity': 1}
    )
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    # Get both counts
    cart_count = cart.items.count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
        
    return JsonResponse({
        'status': 'success',
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'message': f'{product.name} added to cart'
    })

@login_required
@require_POST
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    status = 'added' if created else 'exists'
    message = f'{product.name} added to wishlist' if created else f'{product.name} is already in wishlist'
    
    # Get both counts
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_count = cart.items.count()
    
    return JsonResponse({
        'status': 'success',
        'action': status,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count,
        'message': message
    })

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard_home')
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Authenticate via email
            user_obj = User.objects.filter(email=email).first()
            if user_obj and user_obj.check_password(password):
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    
                    # Redirect admins to dashboard
                    if user.is_staff:
                        return redirect('dashboard_home')
                    
                    # Always redirect regular users to home page, ignore 'next' parameter
                    messages.success(request, f'Welcome back, {user.first_name}! 🐾')
                    return redirect('index')
            
            messages.error(request, 'Invalid email or password.')
        except Exception as e:
            messages.error(request, 'An error occurred during login.')
            
    return render(request, 'furfeast/login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        
        # Check if email already exists in User
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'furfeast/signup.html')
        
        # Check if pending registration exists
        existing_pending = PendingRegistration.objects.filter(email=email).first()
        if existing_pending:
            # Delete old pending registration and create new one with fresh OTP
            existing_pending.delete()
        
        # Check rate limit: max 3 signup attempts in 24 hours
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        recent_attempts = PendingRegistration.objects.filter(
            email=email,
            created_at__gte=twenty_four_hours_ago
        ).count()
        
        if recent_attempts >= 3:
            messages.error(request, 'Too many signup attempts. Please try again after 24 hours.')
            return render(request, 'furfeast/signup.html')
        
        from django.contrib.auth.hashers import make_password
        import random
        
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=10)
        
        pending_reg = PendingRegistration.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password_hash=make_password(password),
            otp=otp,
            expires_at=expires_at
        )
        
        # Send OTP email with HTML
        from django.core.mail import EmailMultiAlternatives
        try:
            subject = 'Verify Your FurFeast Account'
            text_content = f'Your verification code is: {otp}\n\nThis code expires in 10 minutes.\n\nIf you didn\'t request this, please ignore this email.'
            html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #3A5A40 0%, #588157 100%); padding: 40px 20px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: bold;">🐾 FURFEAST</h1>
                            <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">Premium Pet Food & Accessories</p>
                        </td>
                    </tr>
                    
                    <!-- Body -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h2 style="color: #3A5A40; margin: 0 0 20px 0; font-size: 24px;">Verify Your Account</h2>
                            <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                                Hi {first_name},<br><br>
                                Thank you for joining the FurFeast family! To complete your registration, please use the verification code below:
                            </p>
                            
                            <!-- OTP Box -->
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td align="center" style="padding: 20px 0;">
                                        <div style="background-color: #f8f9fa; border: 2px dashed #3A5A40; border-radius: 10px; padding: 20px; display: inline-block;">
                                            <p style="color: #666666; font-size: 14px; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 1px;">Your Verification Code</p>
                                            <p style="color: #3A5A40; font-size: 36px; font-weight: bold; margin: 0; letter-spacing: 8px; font-family: 'Courier New', monospace;">{otp}</p>
                                        </div>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 30px 0 0 0; text-align: center;">
                                ⏰ This code will expire in <strong>10 minutes</strong>
                            </p>
                            
                            <p style="color: #999999; font-size: 13px; line-height: 1.6; margin: 30px 0 0 0; padding-top: 20px; border-top: 1px solid #eeeeee;">
                                If you didn't create an account with FurFeast, please ignore this email or contact our support team if you have concerns.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #eeeeee;">
                            <p style="color: #999999; font-size: 12px; margin: 0 0 10px 0;">
                                © 2024 FurFeast Co. All rights reserved.
                            </p>
                            <p style="color: #999999; font-size: 12px; margin: 0;">
                                Questions? Contact us at <a href="mailto:cofurfeast@gmail.com" style="color: #3A5A40; text-decoration: none;">cofurfeast@gmail.com</a>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
'''
            
            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
            
            # Store email in session for verification page
            request.session['pending_email'] = email
            return redirect('verify_otp')
        except Exception as e:
            pending_reg.delete()
            messages.error(request, f'Failed to send verification email: {str(e)}')
            return render(request, 'furfeast/signup.html')
            
    return render(request, 'furfeast/signup.html')

@login_required
@never_cache
def cart_view(request):
    context = get_context_data(request)
    # Always get fresh cart data with prefetch for better performance
    cart, created = Cart.objects.prefetch_related('items__product').get_or_create(user=request.user)
    context['cart'] = cart
    
    # Add cache control headers
    response = render(request, 'furfeast/cart.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
@never_cache
def profile_view(request):
    context = get_context_data(request)
    # Ensure user profile exists
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get purchase history with filters
    now = timezone.now()
    filter_period = request.GET.get('filter', 'all')
    
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    
    if filter_period == 'week':
        week_start = now - timedelta(days=now.weekday())
        orders = orders.filter(created_at__gte=week_start)
    elif filter_period == 'month':
        month_start = now.replace(day=1)
        orders = orders.filter(created_at__gte=month_start)
    elif filter_period == 'year':
        year_start = now.replace(month=1, day=1)
        orders = orders.filter(created_at__gte=year_start)
    
    context.update({
        'profile': profile,
        'orders': orders,
        'filter_period': filter_period
    })
    
    response = render(request, 'furfeast/profile.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
def order_tracking(request, order_id):
    context = get_context_data(request)
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    context['order'] = order
    return render(request, 'furfeast/order_tracking.html', context)

@login_required
@require_POST
def upload_profile_picture(request):
    try:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            return JsonResponse({
                'success': True, 
                'image_url': profile.profile_picture.url,
                'message': 'Profile picture updated successfully!'
            })
        return JsonResponse({'success': False, 'error': 'No file uploaded'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def delete_profile_picture(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.profile_picture:
            # Delete the file from storage
            profile.profile_picture.delete(save=False)
            # Clear the field in database
            profile.profile_picture = None
            profile.save()
            
        return JsonResponse({
            'success': True,
            'message': 'Profile picture deleted successfully!'
        })
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profile not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def search_products(request):
    context = get_context_data(request)
    query = request.GET.get('q', '').strip()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()
    
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')
    
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context.update({
        'products': page_obj,
        'sort_by': sort_by,
        'search_query': query,
    })
    
    return render(request, 'furfeast/shop.html', context)

def blog_list(request):
    context = get_context_data(request)
    blogs = Blog.objects.filter(is_published=True).order_by('-created_at')
    context['blogs'] = blogs
    return render(request, 'furfeast/blog_list.html', context)

def blog_detail(request, blog_id):
    context = get_context_data(request)
    blog = get_object_or_404(Blog, id=blog_id, is_published=True)
    context['blog'] = blog
    return render(request, 'furfeast/blog_detail.html', context)

def about(request):
    context = get_context_data(request)
    about_us, created = AboutUs.objects.get_or_create(id=1)
    context['about_us'] = about_us
    return render(request, 'furfeast/about.html', context)

def terms(request):
    context = get_context_data(request)
    return render(request, 'furfeast/terms.html', context)

def shipping(request):
    context = get_context_data(request)
    return render(request, 'furfeast/shipping.html', context)

def refund(request):
    context = get_context_data(request)
    return render(request, 'furfeast/refund.html', context)

def contact(request):
    context = get_context_data(request)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to send a message.')
            return redirect('login')
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if first_name and last_name and subject and message:
            ContactMessage.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                email=request.user.email,
                subject=subject,
                message=message
            )
            
            # Send email notification to admin
            try:
                admin_email = 'cofurfeast@gmail.com'
                email_subject = f'New Contact Form Message: {subject}'
                email_message = f'''
New contact form submission from FurFeast website:

From: {first_name} {last_name} ({request.user.email})
Subject: {subject}

Message:
{message}

---
Submitted at: {timezone.now().strftime('%B %d, %Y at %I:%M %p')}
User ID: {request.user.id}
'''
                
                send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_email],
                    fail_silently=True,
                )
            except Exception as e:
                # Log error but don't fail the form submission
                print(f'Failed to send contact form email: {e}')
            
            messages.success(request, 'Your message has been sent successfully! We\'ll get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'furfeast/contact.html', context)

@login_required
@never_cache
def wishlist_view(request):
    context = get_context_data(request)
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    context['wishlist_items'] = wishlist_items
    
    response = render(request, 'furfeast/wishlist.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def logout_view(request):
    logout(request)
    return redirect('index')

@require_POST
def paypal_capture(request):
    print(f"PayPal capture called, user authenticated: {request.user.is_authenticated}")
    if not request.user.is_authenticated:
        print("User not authenticated, returning error")
        return JsonResponse({'success': False, 'error': 'Authentication required'})
    try:
        data = json.loads(request.body)
        print(f"PayPal capture data received: {data}")
        order_id = data.get('orderID')
        payment_id = data.get('paymentID')
        shipping_address = data.get('shipping_address', '').strip()
        shipping_phone = data.get('shipping_phone', '').strip()
        shipping_city = data.get('shipping_city', '').strip()
        shipping_postal_code = data.get('shipping_postal_code', '').strip()
        print(f"Shipping data: {shipping_address}, {shipping_phone}, {shipping_city}, {shipping_postal_code}")
        
        if not order_id:
            return JsonResponse({'success': False, 'error': 'Missing PayPal order ID'})
        
        # Get user's cart
        cart = Cart.objects.get(user=request.user)
        
        if not cart.items.exists():
            return JsonResponse({'success': False, 'error': 'Cart is empty'})
        
        # Validate all items are in stock before processing payment
        for cart_item in cart.items.select_related('product'):
            cart_item.product.refresh_from_db()  # Get latest stock data
            if cart_item.product.is_out_of_stock or cart_item.product.stock == 0:
                return JsonResponse({
                    'success': False, 
                    'error': f'{cart_item.product.name} is out of stock. Please remove it from your cart.'
                })
        
        # Validate total amount
        try:
            total_amount = Decimal(str(cart.total_price)).quantize(Decimal('0.01'))
        except (InvalidOperation, ValueError):
            return JsonResponse({'success': False, 'error': 'Invalid cart total amount'})
        
        # Create order with shipping address
        order = Order.objects.create(
            user=request.user,
            order_id=f'FF{str(uuid.uuid4())[:8].upper()}',
            paypal_payment_id=payment_id or f'PAYPAL_{order_id}',
            status='paid',
            payment_status='paid',
            payment_method='paypal',
            total_amount=total_amount,
            shipping_address=shipping_address,
            shipping_phone=shipping_phone,
            shipping_city=shipping_city,
            shipping_postal_code=shipping_postal_code
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # Clear cart
        cart.items.all().delete()
        
        return JsonResponse({
            'success': True, 
            'order_id': order.order_id,
            'message': f'Payment successful! Order {order.order_id} created.'
        })
        
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart not found'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request data'})
    except Exception as e:
        import traceback
        print(f"PayPal capture error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({'success': False, 'error': f'Payment processing failed: {str(e)}'})

@login_required
@require_POST
def paypal_create_order(request):
    try:
        data = json.loads(request.body)
        amount = data.get('amount')
        
        if not amount:
            return JsonResponse({'error': 'Amount required'}, status=400)
        
        # Create PayPal order via REST API
        import requests
        from django.conf import settings
        
        # Get access token
        auth_response = requests.post(
            f'https://api-m.paypal.com/v1/oauth2/token',
            headers={'Accept': 'application/json', 'Accept-Language': 'en_US'},
            auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
            data={'grant_type': 'client_credentials'}
        )
        
        if auth_response.status_code != 200:
            return JsonResponse({'error': 'PayPal authentication failed'}, status=500)
        
        access_token = auth_response.json()['access_token']
        
        # Create order
        order_response = requests.post(
            f'https://api-m.paypal.com/v2/checkout/orders',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            },
            json={
                'intent': 'CAPTURE',
                'purchase_units': [{
                    'amount': {
                        'currency_code': 'USD',
                        'value': str(amount)
                    },
                    'description': 'FurFeast Pet Products Order'
                }]
            }
        )
        
        if order_response.status_code != 201:
            return JsonResponse({'error': 'Failed to create PayPal order'}, status=500)
        
        order_data = order_response.json()
        return JsonResponse({'orderID': order_data['id']})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def cod_order(request):
    try:
        data = json.loads(request.body)
        shipping_address = data.get('shipping_address', '').strip()
        shipping_phone = data.get('shipping_phone', '').strip()
        shipping_city = data.get('shipping_city', '').strip()
        shipping_postal_code = data.get('shipping_postal_code', '').strip()
        
        if not shipping_address or not shipping_phone or not shipping_city:
            return JsonResponse({'success': False, 'error': 'Please fill in all required address fields'})
        
        # Check if it's a single product order (buy now) or cart order
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        
        if product_id and quantity:
            # Single product order (buy now)
            product = get_object_or_404(Product, id=product_id)
            quantity = int(quantity)
            
            if product.is_out_of_stock or product.stock == 0:
                return JsonResponse({
                    'success': False, 
                    'error': f'{product.name} is out of stock'
                })
            
            if quantity > product.stock:
                return JsonResponse({
                    'success': False, 
                    'error': f'Only {product.stock} items available'
                })
            
            total_amount = product.price * quantity
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                order_id=f'FF{str(uuid.uuid4())[:8].upper()}',
                status='pending',
                payment_status='unpaid',
                payment_method='cod',
                total_amount=total_amount,
                shipping_address=shipping_address,
                shipping_phone=shipping_phone,
                shipping_city=shipping_city,
                shipping_postal_code=shipping_postal_code
            )
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            
        else:
            # Cart order (existing functionality)
            cart = Cart.objects.get(user=request.user)
            
            if not cart.items.exists():
                return JsonResponse({'success': False, 'error': 'Cart is empty'})
            
            # Validate all items are in stock
            for cart_item in cart.items.select_related('product'):
                cart_item.product.refresh_from_db()
                if cart_item.product.is_out_of_stock or cart_item.product.stock == 0:
                    return JsonResponse({
                        'success': False, 
                        'error': f'{cart_item.product.name} is out of stock. Please remove it from your cart.'
                    })
            
            # Create COD order
            order = Order.objects.create(
                user=request.user,
                order_id=f'FF{str(uuid.uuid4())[:8].upper()}',
                status='pending',
                payment_status='unpaid',
                payment_method='cod',
                total_amount=cart.total_price,
                shipping_address=shipping_address,
                shipping_phone=shipping_phone,
                shipping_city=shipping_city,
                shipping_postal_code=shipping_postal_code
            )
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Clear cart
            cart.items.all().delete()
        
        return JsonResponse({
            'success': True, 
            'order_id': order.order_id,
            'message': f'COD order {order.order_id} created successfully!'
        })
        
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart not found'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid request data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Order processing failed: {str(e)}'})

@login_required
@require_POST
def create_paypal_payment(request):
    try:
        # Get user's cart
        cart = Cart.objects.get(user=request.user)
        amount = request.POST.get('amount')
        
        # Validate cart has items
        if not cart.items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('cart')
        
        # Create PayPal payment URL (direct redirect to sandbox)
        paypal_url = f"https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_xclick&business=sb-cb3s248254486@business.example.com&item_name=FurFeast+Order&amount={amount}&currency_code=USD&no_shipping=1&return={request.build_absolute_uri('/paypal-success/')}&cancel_return={request.build_absolute_uri('/cart/')}&notify_url={request.build_absolute_uri('/paypal-success/')}"
        
        return redirect(paypal_url)
        
    except Cart.DoesNotExist:
        messages.error(request, 'Cart not found.')
        return redirect('cart')
    except Exception as e:
        messages.error(request, 'Payment initialization failed. Please try again.')
        return redirect('cart')

@login_required
def paypal_success(request):
    try:
        # Get user's cart
        cart = Cart.objects.get(user=request.user)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            order_id=f'FF{str(uuid.uuid4())[:8].upper()}',
            paypal_payment_id=f'SANDBOX_{timezone.now().strftime("%Y%m%d%H%M%S")}',
            status='paid',
            total_amount=cart.total_price
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, f'Payment successful! Order {order.order_id} created.')
        return redirect('order_success')
        
    except Cart.DoesNotExist:
        messages.error(request, 'Cart not found.')
        return redirect('cart')
    except Exception as e:
        messages.error(request, 'Order processing failed.')
        return redirect('cart')

@login_required
@require_POST
def update_cart_item(request, item_id):
    try:
        # Make sure the cart item exists and belongs to the current user
        cart_item = CartItem.objects.select_related('cart', 'product').get(
            id=item_id, 
            cart__user=request.user
        )
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            # Don't delete item when quantity reaches 1, just keep it at 1
            else:
                return JsonResponse({
                    'success': True,
                    'cart_count': cart.items.count(),
                    'total_price': str(cart.total_price),
                    'wishlist_count': Wishlist.objects.filter(user=request.user).count(),
                    'message': 'Minimum quantity is 1'
                })
        elif action == 'remove':
            cart_item.delete()
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action'})
            
        # Get fresh cart data
        cart = Cart.objects.get(user=request.user)
        
        return JsonResponse({
            'success': True,
            'cart_count': cart.items.count(),
            'total_price': str(cart.total_price),
            'wishlist_count': Wishlist.objects.filter(user=request.user).count()
        })
    except CartItem.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'error': 'Cart item not found or does not belong to you'
        })
    except Cart.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'error': 'Cart not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': f'Server error: {str(e)}'
        })

@login_required
@require_POST
def clear_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        # Delete all cart items
        cart.items.all().delete()
        # Update cart timestamp to ensure fresh data
        cart.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart cleared successfully'
        })
    except Cart.DoesNotExist:
        return JsonResponse({
            'success': True,
            'message': 'Cart was already empty'
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': f'Failed to clear cart: {str(e)}'
        })

@login_required
@require_POST
def update_profile(request):
    try:
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Update or create profile with phone number
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone_number = request.POST.get('phone_number', '')
        profile.save()
        
        return redirect('profile')
    except Exception as e:
        return redirect('profile')

@login_required
@require_POST
def clear_wishlist(request):
    try:
        Wishlist.objects.filter(user=request.user).delete()
        
        return JsonResponse({
            'success': True,
            'wishlist_count': 0
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@require_POST
def remove_from_wishlist(request, product_id):
    try:
        deleted_count, _ = Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
        
        if deleted_count > 0:
            return JsonResponse({
                'success': True,
                'message': 'Item removed from wishlist'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Item not found in wishlist'
            })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': f'Failed to remove item: {str(e)}'
        })

def order_success(request):
    context = get_context_data(request)
    return render(request, 'furfeast/order_success.html', context)

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp', '').strip()
        email = request.session.get('pending_email')
        
        if not email:
            messages.error(request, 'Session expired. Please sign up again.')
            return redirect('signup')
        
        try:
            pending_reg = PendingRegistration.objects.get(email=email)
            
            # Check if OTP expired
            if pending_reg.expires_at < timezone.now():
                pending_reg.delete()
                del request.session['pending_email']
                messages.error(request, 'OTP expired. Please sign up again.')
                return redirect('signup')
            
            # Verify OTP
            if pending_reg.otp == otp:
                # Create user
                username = pending_reg.email.split('@')[0]
                if User.objects.filter(username=username).exists():
                    username = f"{username}_{User.objects.count()}"
                
                user = User.objects.create_user(
                    username=username,
                    email=pending_reg.email,
                    first_name=pending_reg.first_name,
                    last_name=pending_reg.last_name
                )
                user.password = pending_reg.password_hash
                user.is_active = True
                user.save()
                
                # Create profile
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.phone_number = pending_reg.phone_number or ''
                profile.email_verified = True
                profile.save()
                
                # Delete pending registration
                pending_reg.delete()
                del request.session['pending_email']
                
                messages.success(request, 'Account verified successfully! You can now log in. 🐾')
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
        
        except PendingRegistration.DoesNotExist:
            messages.error(request, 'Invalid session. Please sign up again.')
            return redirect('signup')
    
    return render(request, 'furfeast/verify_otp.html')

def verify_email(request, token):
    # Old verification method - kept for backward compatibility
    messages.error(request, 'This verification link is no longer valid. Please sign up again.')
    return redirect('signup')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Generate 6-digit OTP
            import random
            otp = str(random.randint(100000, 999999))
            
            # Store OTP and expiry in profile
            profile.password_reset_token = otp
            profile.password_reset_expires = timezone.now() + timedelta(minutes=10)
            profile.save()
            
            # Send OTP email with HTML
            from django.core.mail import EmailMultiAlternatives
            try:
                subject = 'Reset Your FurFeast Password'
                text_content = f'Your password reset code is: {otp}\n\nThis code expires in 10 minutes.\n\nIf you didn\'t request this, please ignore this email.'
                html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <tr>
                        <td style="background: linear-gradient(135deg, #3A5A40 0%, #588157 100%); padding: 40px 20px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: bold;">🐾 FURFEAST</h1>
                            <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">Premium Pet Food & Accessories</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h2 style="color: #3A5A40; margin: 0 0 20px 0; font-size: 24px;">Reset Your Password</h2>
                            <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                                Hi {user.first_name},<br><br>
                                We received a request to reset your password. Use the code below to reset it:
                            </p>
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td align="center" style="padding: 20px 0;">
                                        <div style="background-color: #f8f9fa; border: 2px dashed #3A5A40; border-radius: 10px; padding: 20px; display: inline-block;">
                                            <p style="color: #666666; font-size: 14px; margin: 0 0 10px 0; text-transform: uppercase; letter-spacing: 1px;">Your Reset Code</p>
                                            <p style="color: #3A5A40; font-size: 36px; font-weight: bold; margin: 0; letter-spacing: 8px; font-family: 'Courier New', monospace;">{otp}</p>
                                        </div>
                                    </td>
                                </tr>
                            </table>
                            <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 30px 0 0 0; text-align: center;">
                                ⏰ This code will expire in <strong>10 minutes</strong>
                            </p>
                            <p style="color: #999999; font-size: 13px; line-height: 1.6; margin: 30px 0 0 0; padding-top: 20px; border-top: 1px solid #eeeeee;">
                                If you didn't request a password reset, please ignore this email or contact our support team if you have concerns.
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #eeeeee;">
                            <p style="color: #999999; font-size: 12px; margin: 0 0 10px 0;">
                                © 2024 FurFeast Co. All rights reserved.
                            </p>
                            <p style="color: #999999; font-size: 12px; margin: 0;">
                                Questions? Contact us at <a href="mailto:cofurfeast@gmail.com" style="color: #3A5A40; text-decoration: none;">cofurfeast@gmail.com</a>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
'''
                
                msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=False)
                
                # Store email in session
                request.session['reset_email'] = email
                messages.success(request, 'Password reset code sent to your email! 📧')
                return redirect('reset_password_otp')
            except Exception as e:
                messages.error(request, f'Failed to send reset email: {str(e)}')
                
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
            
        return redirect('forgot_password')
    
    return render(request, 'furfeast/forgot_password.html')

def reset_password_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp', '').strip()
        email = request.session.get('reset_email')
        
        if not email:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('forgot_password')
        
        try:
            user = User.objects.get(email=email)
            profile = UserProfile.objects.get(user=user)
            
            # Check if OTP expired
            if profile.password_reset_expires < timezone.now():
                profile.password_reset_token = None
                profile.password_reset_expires = None
                profile.save()
                del request.session['reset_email']
                messages.error(request, 'Reset code expired. Please request a new one.')
                return redirect('forgot_password')
            
            # Verify OTP
            if profile.password_reset_token == otp:
                # Store verified email for password reset page
                request.session['verified_reset_email'] = email
                del request.session['reset_email']
                return redirect('reset_password_form')
            else:
                messages.error(request, 'Invalid reset code. Please try again.')
        
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            messages.error(request, 'Invalid session. Please try again.')
            return redirect('forgot_password')
    
    return render(request, 'furfeast/reset_password_otp.html')

def reset_password_form(request):
    email = request.session.get('verified_reset_email')
    if not email:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'furfeast/reset_password_form.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'furfeast/reset_password_form.html')
        
        try:
            user = User.objects.get(email=email)
            profile = UserProfile.objects.get(user=user)
            
            # Reset password
            user.set_password(password)
            user.save()
            
            # Clear reset token
            profile.password_reset_token = None
            profile.password_reset_expires = None
            profile.save()
            
            del request.session['verified_reset_email']
            
            messages.success(request, 'Password reset successfully! You can now log in. 🐾')
            return redirect('login')
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            messages.error(request, 'Invalid session. Please try again.')
            return redirect('forgot_password')
    
    return render(request, 'furfeast/reset_password_form.html')

def reset_password(request, token):
    try:
        profile = UserProfile.objects.get(
            password_reset_token=token,
            password_reset_expires__gt=timezone.now()
        )
        
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'furfeast/reset_password.html', {'token': token})
            
            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, 'furfeast/reset_password.html', {'token': token})
            
            # Reset password
            profile.user.set_password(password)
            profile.user.save()
            
            # Clear reset token
            profile.password_reset_token = None
            profile.password_reset_expires = None
            profile.save()
            
            messages.success(request, 'Password reset successfully! You can now log in. 🐾')
            return redirect('login')
            
        return render(request, 'furfeast/reset_password.html', {'token': token})
        
    except UserProfile.DoesNotExist:
        messages.error(request, 'Invalid or expired reset token.')
        return redirect('forgot_password')

@require_POST
def join_furfeast_family(request):
    if not request.user.is_authenticated:
        return redirect('signup')
    
    email = request.POST.get('email')
    if email != request.user.email:
        messages.error(request, 'Please use your registered email address.')
        return redirect('index')
    
    return redirect('furfeast_family_form')

def furfeast_family_form(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Check if user already joined
    if FurFeastFamily.objects.filter(user=request.user).exists():
        messages.info(request, 'You are already a member of the FurFeast Family! 🐾')
        return redirect('index')
    
    context = get_context_data(request)
    
    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        pet_category = request.POST.get('pet_category')
        pet_age = request.POST.get('pet_age')
        favourite_food = request.POST.get('favourite_food')
        additional_description = request.POST.get('additional_description', '')
        receive_expert_emails = request.POST.get('receive_expert_emails') == 'on'
        
        FurFeastFamily.objects.create(
            user=request.user,
            pet_name=pet_name,
            pet_category=pet_category,
            pet_age=pet_age,
            favourite_food=favourite_food,
            additional_description=additional_description,
            receive_expert_emails=receive_expert_emails
        )
        
        messages.success(request, f'Welcome to the FurFeast Family! {pet_name} is now part of our community! 🐾')
        return redirect('index')
    
    return render(request, 'furfeast/furfeast_family_form.html', context)

def product_detail(request, product_id):
    context = get_context_data(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Get reviews with average rating
    reviews = Review.objects.filter(product=product).select_related('user').order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Always update product rating to ensure consistency
    if avg_rating != product.rating:
        product.rating = round(avg_rating, 1)
        product.save()
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:8]
    
    context.update({
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': reviews.count(),
        'related_products': related_products,
    })
    
    return render(request, 'furfeast/product_detail.html', context)

@login_required
@require_POST
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user already reviewed this product
    if Review.objects.filter(product=product, user=request.user).exists():
        return JsonResponse({
            'success': False,
            'error': 'You have already reviewed this product'
        })
    
    try:
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment', '').strip()
        
        if rating < 1 or rating > 5:
            return JsonResponse({
                'success': False,
                'error': 'Rating must be between 1 and 5'
            })
        
        if not comment:
            return JsonResponse({
                'success': False,
                'error': 'Comment is required'
            })
        
        # Create the review
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
        
        # Update product rating immediately
        reviews = Review.objects.filter(product=product)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        product.rating = round(avg_rating, 1)
        product.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Review added successfully!',
            'new_rating': product.rating,
            'review_count': reviews.count()
        })
        
    except (ValueError, TypeError):
        return JsonResponse({
            'success': False,
            'error': 'Invalid rating value'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Failed to add review'
        })

@login_required
@require_POST
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    try:
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment', '').strip()
        
        if rating < 1 or rating > 5:
            return JsonResponse({'success': False, 'error': 'Rating must be between 1 and 5'})
        
        if not comment:
            return JsonResponse({'success': False, 'error': 'Comment is required'})
        
        review.rating = rating
        review.comment = comment
        review.save()
        
        # Update product rating
        reviews = Review.objects.filter(product=review.product)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        review.product.rating = round(avg_rating, 1)
        review.product.save()
        
        return JsonResponse({'success': True, 'message': 'Review updated successfully!'})
        
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'error': 'Invalid rating value'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Failed to update review'})

@login_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product = review.product
    
    try:
        review.delete()
        
        # Update product rating
        reviews = Review.objects.filter(product=product)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        product.rating = round(avg_rating, 1)
        product.save()
        
        return JsonResponse({'success': True, 'message': 'Review deleted successfully!'})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Failed to delete review'})

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.is_out_of_stock or product.stock == 0:
        messages.error(request, f'{product.name} is currently out of stock')
        return redirect('product_detail', product_id=product_id)
    
    context = get_context_data(request)
    context.update({
        'product': product,
        'is_buy_now': True,
    })
    
    return render(request, 'furfeast/checkout.html', context)
    product = get_object_or_404(Product, id=product_id)
    
    if product.is_out_of_stock or product.stock == 0:
        messages.error(request, f'{product.name} is currently out of stock')
        return redirect('product_detail', product_id=product_id)
    
    context = get_context_data(request)
    context.update({
        'product': product,
        'is_buy_now': True,
    })
    
    return render(request, 'furfeast/checkout.html', context)

@login_required
def test_notification(request):
    """Test view to manually trigger notification creation"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        # Find first order that can be tested
        order = Order.objects.filter(status__in=['pending', 'paid', 'processing']).first()
        if not order:
            return JsonResponse({'error': 'No testable orders found'})
        
        # Count notifications before
        notifications_before = Notification.objects.filter(user=order.user).count()
        
        # Change status to shipped to trigger notification
        order.status = 'shipped'
        order.tracking_number = 'TEST123456'
        order.courier_name = 'Test Courier'
        order.save()
        
        # Count notifications after
        notifications_after = Notification.objects.filter(user=order.user).count()
        latest_notification = Notification.objects.filter(user=order.user).order_by('-created_at').first()
        
        return JsonResponse({
            'success': True,
            'order_id': order.order_id,
            'user': order.user.username,
            'notifications_before': notifications_before,
            'notifications_after': notifications_after,
            'notification_created': notifications_after > notifications_before,
            'latest_notification': {
                'title': latest_notification.title if latest_notification else None,
                'message': latest_notification.message if latest_notification else None
            } if latest_notification else None
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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

# Notification API endpoints
@login_required
@never_cache
def notifications_api(request):
    """API endpoint to get user notifications"""
    seven_days_ago = timezone.now() - timedelta(days=7)
    notifications = Notification.objects.filter(
        user=request.user,
        created_at__gte=seven_days_ago
    ).order_by('-created_at')
    
    unread_count = notifications.filter(is_read=False).count()
    
    response = JsonResponse({
        'count': unread_count,
        'notifications': [{
            'id': n.id,
            'title': n.title,
            'message': 'You have got message from Seller' if n.notification_type == 'message' else n.message,
            'link': n.link,
            'is_read': n.is_read,
            'notification_type': n.notification_type,
            'created_at': timezone.localtime(n.created_at).strftime('%b %d, %Y at %I:%M %p')
        } for n in notifications[:20]]
    })
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'})

@login_required
@require_POST
@never_cache
def clear_all_notifications(request):
    """Delete all notifications for the user"""
    Notification.objects.filter(user=request.user).delete()
    response = JsonResponse({'success': True})
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
@never_cache
def customer_chat(request):
    """Customer chat with seller"""
    from .models import ChatRoom
    context = get_context_data(request)
    chat_room, created = ChatRoom.objects.get_or_create(customer=request.user)
    chat_messages = chat_room.messages.all()
    chat_room.messages.filter(is_from_admin=True, is_read=False).update(is_read=True)
    context['chat_room'] = chat_room
    context['chat_messages'] = chat_messages
    
    response = render(request, 'furfeast/customer_chat.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
@require_POST
def send_customer_message(request):
    """Send message from customer to seller"""
    from .models import ChatRoom
    try:
        message = request.POST.get('message', '').strip()
        image = request.FILES.get('image')
        
        if not message and not image:
            return JsonResponse({'success': False, 'error': 'Message or image required'})
        
        chat_room, _ = ChatRoom.objects.get_or_create(customer=request.user)
        CustomerMessage.objects.create(
            chat_room=chat_room,
            message=message,
            image=image,
            is_from_admin=False
        )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def get_customer_messages(request):
    """Get new messages for customer"""
    from .models import ChatRoom
    after_id = request.GET.get('after', 0)
    chat_room, _ = ChatRoom.objects.get_or_create(customer=request.user)
    messages = chat_room.messages.filter(id__gt=after_id).order_by('created_at')
    
    chat_room.messages.filter(is_from_admin=True, is_read=False).update(is_read=True)
    Notification.objects.filter(user=request.user, notification_type='message', is_read=False).update(is_read=True)
    
    return JsonResponse({
        'messages': [{
            'id': msg.id,
            'message': msg.message,
            'image': msg.image.url if msg.image else None,
            'is_from_admin': msg.is_from_admin,
            'created_at': msg.created_at.isoformat()
        } for msg in messages]
    })



@login_required
def customer_unread_message_count(request):
    """Count unread admin messages for customer"""
    from .models import ChatRoom
    try:
        chat_room = ChatRoom.objects.get(customer=request.user)
        count = chat_room.messages.filter(is_from_admin=True, is_read=False).count()
    except ChatRoom.DoesNotExist:
        count = 0
    return JsonResponse({'count': count})

# Chatbot Views

def chatbot_widget(request):
    """Render chatbot widget"""
    context = get_context_data(request)
    return render(request, 'furfeast/improved_chatbot_widget.html', context)

@csrf_exempt
@require_POST
def chatbot_message(request):
    """Process chatbot message"""
    from .chatbot import chatbot
    import json
    
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        user = request.user if request.user.is_authenticated else None
        result = chatbot.process_message(message, user, session_id)
        
        return JsonResponse({
            'response': result['response'],
            'intent': result['intent'],
            'session_id': result['session_id']
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def chatbot_history(request, session_id):
    """Get chatbot conversation history"""
    from .models import ChatBotSession
    
    try:
        session = ChatBotSession.objects.get(session_id=session_id)
        conversations = session.conversations.all()[:20]
        
        return JsonResponse({
            'conversations': [{
                'user_message': conv.user_message,
                'bot_response': conv.bot_response,
                'created_at': conv.created_at.isoformat()
            } for conv in conversations]
        })
        
    except ChatBotSession.DoesNotExist:
        return JsonResponse({'conversations': []})

# Chatbot Testing Views

def chatbot_test_view(request):
    """Test view for chatbot responsiveness across different devices"""
    context = {
        'title': 'Chatbot Test - FurFeast',
        'test_devices': [
            {'name': 'iPhone SE', 'width': 375, 'height': 667},
            {'name': 'iPhone 12', 'width': 390, 'height': 844},
            {'name': 'Samsung Galaxy S21', 'width': 360, 'height': 800},
            {'name': 'iPad', 'width': 768, 'height': 1024},
            {'name': 'iPad Pro', 'width': 1024, 'height': 1366},
            {'name': 'Desktop', 'width': 1920, 'height': 1080},
        ]
    }
    return render(request, 'furfeast/chatbot_test.html', context)

@csrf_exempt
@require_POST
def chatbot_test_message(request):
    """Test endpoint for chatbot messages"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        
        # Simulate different types of responses for testing
        test_responses = {
            'hello': 'Hello! Welcome to FurFeast! 🐾 How can I help you today?',
            'products': 'We have a wide range of premium pet food and accessories:\n• Dog Food (Dry & Wet)\n• Cat Food (Dry & Wet)\n• Treats & Snacks\n• Toys & Accessories\n• Health & Wellness Products',
            'shipping': 'Our shipping rates are:\n• Standard Delivery (3-5 days): $5.99\n• Express Delivery (1-2 days): $12.99\n• Free shipping on orders over $50!',
            'payment': 'We accept:\n• Credit/Debit Cards (Visa, MasterCard, American Express)\n• PayPal\n• Apple Pay\n• Google Pay\n• Bank Transfer',
            'support': 'You can reach our support team:\n📞 Phone: 1-800-FURFEAST\n📧 Email: support@furfeast.com\n💬 Live Chat: Available 24/7\n🕒 Business Hours: Mon-Fri 9AM-6PM EST',
        }
        
        # Find appropriate response
        message_lower = message.lower()
        response = None
        
        for keyword, reply in test_responses.items():
            if keyword in message_lower:
                response = reply
                break
        
        if not response:
            if len(message) > 100:
                response = "I understand you have a detailed question. Let me connect you with our support team for personalized assistance!"
            elif any(word in message_lower for word in ['help', 'assist', 'support']):
                response = "I'm here to help! You can ask me about our products, shipping, payments, or anything else related to FurFeast."
            else:
                response = f"Thanks for your message: '{message}'. I'm still learning, but I can help you with information about our products, shipping, payments, and support. What would you like to know?"
        
        return JsonResponse({
            'response': response,
            'session_id': 'test_session_123',
            'timestamp': '2024-01-01T12:00:00Z'
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'Sorry, I encountered an error processing your message.',
            'details': str(e)
        }, status=500)
