from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.db import models
import json
from .models import Product, FlashSale, PromoCode, Blog, AboutUs, MassEmailCampaign, Order, HeroImage, FurFeastFamily, Notification, ContactMessage, CustomerMessage
from django.core.paginator import Paginator
from PIL import Image as PILImage
from django.core.files.base import ContentFile
import io

# Helper to check if user is staff (admin)
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Image processing utility for hero images
def process_hero_image(image_file):
    """Process uploaded image to 1920x800 dimensions"""
    try:
        # Open image
        img = PILImage.open(image_file)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get original dimensions
        original_width, original_height = img.size
        target_width, target_height = 1920, 800
        
        # Calculate aspect ratios
        original_ratio = original_width / original_height
        target_ratio = target_width / target_height
        
        if original_ratio > target_ratio:
            # Image is wider - resize by height and crop width
            new_height = target_height
            new_width = int(original_width * (target_height / original_height))
            img = img.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
            
            # Crop from center
            left = (new_width - target_width) // 2
            img = img.crop((left, 0, left + target_width, target_height))
        else:
            # Image is taller - resize by width and crop height
            new_width = target_width
            new_height = int(original_height * (target_width / original_width))
            img = img.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
            
            # Crop from center
            top = (new_height - target_height) // 2
            img = img.crop((0, top, target_width, top + target_height))
        
        # Save processed image to memory
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=95, optimize=True)
        output.seek(0)
        
        # Create ContentFile
        processed_file = ContentFile(output.getvalue())
        processed_file.name = image_file.name
        
        return processed_file
        
    except Exception as e:
        raise ValidationError(f"Error processing image: {str(e)}")

@user_passes_test(is_admin)
def dashboard_home(request):
    """Main dashboard overview"""
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    
    # Get order statistics
    all_orders = Order.objects.all()
    total_orders = all_orders.count()
    pending_orders = all_orders.filter(status='pending').count()
    
    # Get recent orders with filtering
    recent_orders = Order.objects.select_related('user').order_by('-created_at')
    if status_filter != 'all':
        recent_orders = recent_orders.filter(status=status_filter)
    recent_orders = recent_orders[:10]  # Show last 10 orders
    
    context = {
        'total_products': Product.objects.count(),
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_users': User.objects.count(),
        'recent_orders': recent_orders,
        'status_filter': status_filter
    }
    return render(request, 'furfeast/dashboard/admindashboard.html', context)

@user_passes_test(is_admin)
@require_POST
def update_order_status_ajax(request):
    """AJAX endpoint for updating order status from dashboard"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        new_status = data.get('status')
        
        if not order_id or not new_status:
            return JsonResponse({'success': False, 'error': 'Missing order ID or status'})
        
        order = get_object_or_404(Order, id=order_id)
        
        if new_status not in dict(Order.STATUS_CHOICES):
            return JsonResponse({'success': False, 'error': 'Invalid status'})
        
        old_status = order.status
        order.status = new_status
        
        # Update timestamps based on status
        if new_status == 'shipped' and old_status != 'shipped':
            order.shipped_at = timezone.now()
        elif new_status == 'delivered' and old_status != 'delivered':
            order.delivered_at = timezone.now()
        
        order.save()
        
        # Create notification for customer
        if old_status != new_status:
            status_messages = {
                'processing': f'Your order #{order.order_id} is now being processed! 📦',
                'shipped': f'Great news! Your order #{order.order_id} has been shipped! 🚚',
                'delivered': f'Your order #{order.order_id} has been delivered! Enjoy your purchase! 🎉',
                'cancelled': f'Your order #{order.order_id} has been cancelled. Contact us if you have questions. ❌'
            }
            
            if new_status in status_messages:
                Notification.objects.create(
                    user=order.user,
                    title=f'Order {order.get_status_display()}',
                    message=status_messages[new_status],
                    order=order,
                    link=f'/order-tracking/{order.order_id}/',
                    notification_type='order'
                )
        
        return JsonResponse({
            'success': True, 
            'message': f'Order {order.order_id} status updated to {order.get_status_display()}'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@user_passes_test(is_admin)
def order_list(request):
    orders = Order.objects.select_related('user', 'user__profile').prefetch_related('items__product').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Get status counts for dashboard
    all_orders = Order.objects.all()
    pending_count = all_orders.filter(status='pending').count()
    processing_count = all_orders.filter(status='processing').count()
    shipped_count = all_orders.filter(status='shipped').count()
    delivered_count = all_orders.filter(status='delivered').count()
    
    paginator = Paginator(orders, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'orders': page_obj,
        'status_filter': status_filter,
        'status_choices': Order.STATUS_CHOICES,
        'pending_count': pending_count,
        'processing_count': processing_count,
        'shipped_count': shipped_count,
        'delivered_count': delivered_count,
    }
    return render(request, 'furfeast/dashboard/order_list.html', context)

@user_passes_test(is_admin)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'furfeast/dashboard/order_detail.html', context)

@user_passes_test(is_admin)
def order_update_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        tracking_number = request.POST.get('tracking_number', '').strip()
        courier_name = request.POST.get('courier_name', '').strip()
        admin_notes = request.POST.get('admin_notes', '').strip()
        
        if new_status in dict(Order.STATUS_CHOICES):
            old_status = order.status
            order.status = new_status
            
            # Update timestamps based on status
            if new_status == 'shipped' and old_status != 'shipped':
                order.shipped_at = timezone.now()
            elif new_status == 'delivered' and old_status != 'delivered':
                order.delivered_at = timezone.now()
            
            # Update shipping info if provided
            if tracking_number:
                order.tracking_number = tracking_number
            if courier_name:
                order.courier_name = courier_name
            if admin_notes:
                order.admin_notes = admin_notes
            
            order.save()
            
            # Create notification for customer
            if old_status != new_status:
                status_messages = {
                    'processing': f'Your order #{order.order_id} is now being processed! 📦',
                    'shipped': f'Great news! Your order #{order.order_id} has been shipped! 🚚',
                    'delivered': f'Your order #{order.order_id} has been delivered! Enjoy your purchase! 🎉',
                    'cancelled': f'Your order #{order.order_id} has been cancelled. Contact us if you have questions. ❌'
                }
                
                if new_status in status_messages:
                    Notification.objects.create(
                        user=order.user,
                        title=f'Order {order.get_status_display()}',
                        message=status_messages[new_status],
                        order=order,
                        link=f'/order-tracking/{order.order_id}/',
                        notification_type='order'
                    )
            
            messages.success(request, f'Order {order.order_id} status updated to {order.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status selected.')
    
    # Check if request came from detail page
    if 'dashboard/orders/' in request.META.get('HTTP_REFERER', '') and '/update-status/' not in request.META.get('HTTP_REFERER', ''):
        return redirect('dashboard_order_detail', order_id=order_id)
    else:
        # Add timestamp to force refresh of counts
        import time
        return redirect(f'/dashboard/orders/?refresh={int(time.time())}')

# Notification endpoints
@login_required
def get_notifications(request):
    notifications = request.user.notifications.filter(is_read=False)[:5]
    return JsonResponse({
        'notifications': [{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'created_at': n.created_at.strftime('%b %d, %Y %I:%M %p')
        } for n in notifications],
        'count': notifications.count()
    })

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    try:
        notification = request.user.notifications.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except:
        return JsonResponse({'success': False})

@login_required
@require_POST
def clear_all_notifications(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'success': True})

@user_passes_test(is_admin)
def product_list(request):
    # Get filter parameter
    limit = request.GET.get('limit', 'all')
    
    products_list = Product.objects.all().order_by('-created_at')
    
    # Apply limit filter
    if limit != 'all':
        try:
            limit_num = int(limit)
            products_list = products_list[:limit_num]
        except ValueError:
            pass
    
    # Force fresh data from database
    for product in products_list:
        product.refresh_from_db()
    
    paginator = Paginator(products_list, 20)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'products': products,
        'current_limit': limit
    }
    return render(request, 'furfeast/dashboard/product_list.html', context)

@user_passes_test(is_admin)
def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        original_price = request.POST.get('original_price') or None
        category = request.POST.get('category')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        is_bestseller = request.POST.get('is_bestseller') == 'on'
        image = request.FILES.get('image')
        rating = request.POST.get('rating', 0.0)
        is_out_of_stock = request.POST.get('is_out_of_stock') == 'on'

        slug = slugify(name)
        # Handle duplicate slugs
        if Product.objects.filter(slug=slug).exists():
            messages.error(request, 'Product with this name already exists.')
            return redirect('dashboard_product_create')

        Product.objects.create(
            name=name, slug=slug, price=price, original_price=original_price, category=category,
            description=description, stock=stock, is_bestseller=is_bestseller,
            is_out_of_stock=is_out_of_stock, rating=rating,
            image=image
        )
        messages.success(request, 'Product created successfully.')
        return redirect('dashboard_product_list')
    
    return render(request, 'furfeast/dashboard/product_form.html')

@user_passes_test(is_admin)
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.original_price = request.POST.get('original_price') or None
        product.category = request.POST.get('category')
        product.description = request.POST.get('description')
        product.stock = request.POST.get('stock')
        product.is_bestseller = request.POST.get('is_bestseller') == 'on'
        product.is_out_of_stock = request.POST.get('is_out_of_stock') == 'on'
        product.rating = request.POST.get('rating', 0.0)
        
        # Handle image deletion
        if request.POST.get('delete_image') == 'true':
            if product.image:
                product.image.delete(save=False)
                product.image = None
        
        # Handle new image upload
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        try:
            product.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('dashboard_product_list')
        except ValidationError as e:
            if 'is_out_of_stock' in str(e) or 'stock' in str(e):
                messages.error(request, 'Cannot mark item as out of stock when stock quantity is greater than 0. Please set stock to 0 or uncheck "Out of Stock".')
            else:
                messages.error(request, f'Validation error: {str(e)}')
            return render(request, 'furfeast/dashboard/product_form.html', {'product': product})

    return render(request, 'furfeast/dashboard/product_form.html', {'product': product})

@user_passes_test(is_admin)
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('dashboard_product_list')

# --- Flash Sale Management ---

@user_passes_test(is_admin)
def flash_sale_list(request):
    sales = FlashSale.objects.all().order_by('-start_time')
    return render(request, 'furfeast/dashboard/flash_sale_list.html', {'sales': sales})

@user_passes_test(is_admin)
def flash_sale_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category') or None
        discount = request.POST.get('discount_percentage')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')
        
        FlashSale.objects.create(
            title=title,
            category=category,
            discount_percentage=discount,
            start_time=start,
            end_time=end
        )
        messages.success(request, 'Flash sale created.')
        return redirect('dashboard_flash_sale_list')
    
    return render(request, 'furfeast/dashboard/flash_sale_form.html')

@user_passes_test(is_admin)
def flash_sale_edit(request, sale_id):
    sale = get_object_or_404(FlashSale, id=sale_id)
    if request.method == 'POST':
        sale.title = request.POST.get('title')
        sale.category = request.POST.get('category') or None
        sale.discount_percentage = request.POST.get('discount_percentage')
        sale.start_time = request.POST.get('start_time')
        sale.end_time = request.POST.get('end_time')
        sale.is_active = request.POST.get('is_active') == 'on'
        sale.save()
        messages.success(request, 'Flash sale updated.')
        return redirect('dashboard_flash_sale_list')
    
    return render(request, 'furfeast/dashboard/flash_sale_form.html', {'sale': sale})

@user_passes_test(is_admin)
def flash_sale_delete(request, sale_id):
    sale = get_object_or_404(FlashSale, id=sale_id)
    sale.delete()
    messages.success(request, 'Flash sale deleted.')
    return redirect('dashboard_flash_sale_list')

# --- Promo Code Management ---

@user_passes_test(is_admin)
def promo_code_list(request):
    codes = PromoCode.objects.all().order_by('-valid_from')
    return render(request, 'furfeast/dashboard/promo_code_list.html', {'codes': codes})

@user_passes_test(is_admin)
def promo_code_create(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        amount = request.POST.get('discount_amount')
        min_amount = request.POST.get('min_order_amount', 50.00)
        start_str = request.POST.get('valid_from')
        end_str = request.POST.get('valid_to')

        from datetime import datetime
        start = timezone.make_aware(datetime.strptime(start_str, '%Y-%m-%dT%H:%M'))
        end = timezone.make_aware(datetime.strptime(end_str, '%Y-%m-%dT%H:%M'))

        PromoCode.objects.create(
            code=code,
            discount_amount=amount,
            min_order_amount=min_amount,
            valid_from=start,
            valid_to=end,
            active=True
        )
        messages.success(request, 'Promo code created.')
        return redirect('dashboard_promo_code_list')
        
    return render(request, 'furfeast/dashboard/promo_code_form.html')

@user_passes_test(is_admin)
def promo_code_edit(request, code_id):
    promo = get_object_or_404(PromoCode, id=code_id)
    if request.method == 'POST':
        promo.code = request.POST.get('code')
        promo.discount_amount = request.POST.get('discount_amount')
        promo.min_order_amount = request.POST.get('min_order_amount', 50.00)
        start_str = request.POST.get('valid_from')
        end_str = request.POST.get('valid_to')

        from datetime import datetime
        promo.valid_from = timezone.make_aware(datetime.strptime(start_str, '%Y-%m-%dT%H:%M'))
        promo.valid_to = timezone.make_aware(datetime.strptime(end_str, '%Y-%m-%dT%H:%M'))
        promo.active = request.POST.get('active') == 'on'
        promo.save()
        messages.success(request, 'Promo code updated.')
        return redirect('dashboard_promo_code_list')
    
    return render(request, 'furfeast/dashboard/promo_code_form.html', {'promo': promo})

@user_passes_test(is_admin)
def promo_code_delete(request, code_id):
    promo = get_object_or_404(PromoCode, id=code_id)
    promo.delete()
    messages.success(request, 'Promo code deleted.')
    return redirect('dashboard_promo_code_list')

# --- Blog Management ---

@user_passes_test(is_admin)
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'furfeast/dashboard/blog_list.html', {'blogs': blogs})

@user_passes_test(is_admin)
def blog_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        writer_name = request.POST.get('writer_name', '').strip()
        content = request.POST.get('content')
        image = request.FILES.get('image')
        is_published = request.POST.get('is_published') == 'on'
        image_position_x = request.POST.get('image_position_x', 50.0)
        image_position_y = request.POST.get('image_position_y', 50.0)
        
        slug = slugify(title)
        if Blog.objects.filter(slug=slug).exists():
            messages.error(request, 'Blog with this title already exists.')
            return redirect('dashboard_blog_create')

        Blog.objects.create(
            title=title, slug=slug, content=content, image=image,
            is_published=is_published, author=request.user,
            writer_name=writer_name,
            image_position_x=image_position_x, image_position_y=image_position_y
        )
        messages.success(request, 'Blog post created.')
        return redirect('dashboard_blog_list')
        
    return render(request, 'furfeast/dashboard/blog_form.html')

@user_passes_test(is_admin)
def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.writer_name = request.POST.get('writer_name', '').strip()
        blog.content = request.POST.get('content')
        blog.is_published = request.POST.get('is_published') == 'on'
        blog.image_position_x = request.POST.get('image_position_x', 50.0)
        blog.image_position_y = request.POST.get('image_position_y', 50.0)
        
        if 'image' in request.FILES:
            blog.image = request.FILES['image']
        
        blog.save()
        messages.success(request, 'Blog post updated.')
        return redirect('dashboard_blog_list')

    return render(request, 'furfeast/dashboard/blog_form.html', {'blog': blog})

@user_passes_test(is_admin)
def blog_delete(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    messages.success(request, 'Blog post deleted.')
    return redirect('dashboard_blog_list')

# --- Admin User Management ---

@user_passes_test(is_admin)
def admin_list(request):
    admins = User.objects.filter(is_staff=True).order_by('username')
    return render(request, 'furfeast/dashboard/admin_list.html', {'admins': admins})

@user_passes_test(is_admin)
def admin_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('dashboard_admin_create')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('dashboard_admin_create')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = True # Make them admin
        user.save()
        
        messages.success(request, f'Admin user {username} created successfully.')
        return redirect('dashboard_admin_list')
        
    return render(request, 'furfeast/dashboard/admin_create.html')

@user_passes_test(is_admin)
def admin_edit(request, admin_id):
    admin_user = get_object_or_404(User, id=admin_id, is_staff=True)
    if request.method == 'POST':
        admin_user.username = request.POST.get('username')
        admin_user.email = request.POST.get('email')
        password = request.POST.get('password')
        
        if password:
            from django.contrib.auth.password_validation import validate_password
            try:
                validate_password(password, admin_user)
                admin_user.set_password(password)
            except Exception as e:
                messages.error(request, f'Password validation failed: {str(e)}')
                return render(request, 'furfeast/dashboard/admin_create.html', {'admin_user': admin_user})
        
        admin_user.save()
        messages.success(request, f'Admin user {admin_user.username} updated successfully.')
        return redirect('dashboard_admin_list')
    
    return render(request, 'furfeast/dashboard/admin_create.html', {'admin_user': admin_user})

@user_passes_test(is_admin)
def admin_delete(request, admin_id):
    admin_user = get_object_or_404(User, id=admin_id, is_staff=True)
    admin_user.delete()
    messages.success(request, 'Admin user deleted successfully.')
    return redirect('dashboard_admin_list')

# --- About Us Management ---

@user_passes_test(is_admin)
def about_us_edit(request):
    about_us, created = AboutUs.objects.get_or_create(id=1)
    if request.method == 'POST':
        about_us.title = request.POST.get('title')
        about_us.content = request.POST.get('content')
        about_us.happy_pet_parents_count = request.POST.get('happy_pet_parents_count')
        if 'image' in request.FILES:
            about_us.image = request.FILES['image']
        about_us.save()
        messages.success(request, 'About Us section updated successfully.')
        return redirect('dashboard_home')
    return render(request, 'furfeast/dashboard/about_us_form.html', {'about_us': about_us})

# --- Hero Image Management ---

@user_passes_test(is_admin)
def hero_image_list(request):
    images = HeroImage.objects.all().order_by('order')
    return render(request, 'furfeast/dashboard/hero_image_list.html', {'images': images})

@user_passes_test(is_admin)
def hero_image_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        headline = request.POST.get('headline')
        subheadline = request.POST.get('subheadline')
        cta_text = request.POST.get('cta_text', 'Shop Now')
        cta_link = request.POST.get('cta_link', '/shop/')
        align = request.POST.get('align', 'left')
        order = request.POST.get('order', 0)
        text_position_y = request.POST.get('text_position_y', 50)
        text_position_x = request.POST.get('text_position_x', 10)
        apply_to_all = request.POST.get('apply_position_to_all') == 'true'
        
        # Get images
        desktop_image = request.FILES.get('desktop_image')
        mobile_image = request.FILES.get('mobile_image')
        legacy_image = request.FILES.get('image')  # For backward compatibility
        
        # Validate that at least desktop image is provided
        if not desktop_image and not legacy_image:
            messages.error(request, 'Desktop image is required.')
            return render(request, 'furfeast/dashboard/hero_image_form.html')
        
        try:
            # Process desktop image
            processed_desktop_image = None
            if desktop_image:
                if desktop_image.size < 100 * 1024:  # 100KB
                    messages.error(request, 'Desktop image file must be at least 100KB in size.')
                    return render(request, 'furfeast/dashboard/hero_image_form.html')
                
                if desktop_image.size > 10 * 1024 * 1024:  # 10MB
                    messages.error(request, 'Desktop image file must be less than 10MB in size.')
                    return render(request, 'furfeast/dashboard/hero_image_form.html')
                
                processed_desktop_image = process_hero_image(desktop_image)
            
            # Process mobile image (no resizing, just validation)
            processed_mobile_image = None
            if mobile_image:
                if mobile_image.size < 100 * 1024:  # 100KB
                    messages.error(request, 'Mobile image file must be at least 100KB in size.')
                    return render(request, 'furfeast/dashboard/hero_image_form.html')
                
                if mobile_image.size > 10 * 1024 * 1024:  # 10MB
                    messages.error(request, 'Mobile image file must be less than 10MB in size.')
                    return render(request, 'furfeast/dashboard/hero_image_form.html')
                
                processed_mobile_image = mobile_image
            
            # Process legacy image if provided
            processed_legacy_image = None
            if legacy_image:
                processed_legacy_image = process_hero_image(legacy_image)
            
            hero_image = HeroImage.objects.create(
                title=title, 
                image=processed_legacy_image or processed_desktop_image,  # Fallback to desktop for legacy field
                desktop_image=processed_desktop_image,
                mobile_image=processed_mobile_image,
                headline=headline, 
                subheadline=subheadline,
                cta_text=cta_text, 
                cta_link=cta_link, 
                align=align, 
                order=order,
                text_position_y=text_position_y, 
                text_position_x=text_position_x, 
                is_active=request.POST.get('is_active') == 'on'
            )
            
            # Apply position to all hero images if requested
            if apply_to_all:
                HeroImage.objects.exclude(id=hero_image.id).update(
                    text_position_y=text_position_y, text_position_x=text_position_x
                )
                messages.success(request, f'Hero image created and text position applied to all hero images.')
            else:
                messages.success(request, 'Hero image created successfully with responsive images.')
            
            return redirect('dashboard_hero_image_list')
            
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'furfeast/dashboard/hero_image_form.html')
    
    return render(request, 'furfeast/dashboard/hero_image_form.html')

@user_passes_test(is_admin)
def hero_image_edit(request, image_id):
    hero_image = get_object_or_404(HeroImage, id=image_id)
    if request.method == 'POST':
        hero_image.title = request.POST.get('title')
        hero_image.headline = request.POST.get('headline')
        hero_image.subheadline = request.POST.get('subheadline')
        hero_image.cta_text = request.POST.get('cta_text', 'Shop Now')
        hero_image.cta_link = request.POST.get('cta_link', '/shop/')
        hero_image.align = request.POST.get('align', 'left')
        hero_image.order = request.POST.get('order', 0)
        hero_image.text_position_y = request.POST.get('text_position_y', 50)
        hero_image.text_position_x = request.POST.get('text_position_x', 10)
        hero_image.is_active = request.POST.get('is_active') == 'on'
        apply_to_all = request.POST.get('apply_position_to_all') == 'true'
        
        # Handle desktop image update
        if 'desktop_image' in request.FILES:
            desktop_image = request.FILES['desktop_image']
            
            # Validate file size (100KB minimum, 10MB maximum)
            if desktop_image.size < 100 * 1024:  # 100KB
                messages.error(request, 'Desktop image file must be at least 100KB in size.')
                return render(request, 'furfeast/dashboard/hero_image_form.html', {'hero_image': hero_image})
            
            if desktop_image.size > 10 * 1024 * 1024:  # 10MB
                messages.error(request, 'Desktop image file must be less than 10MB in size.')
                return render(request, 'furfeast/dashboard/hero_image_form.html', {'hero_image': hero_image})
            
            try:
                # Process desktop image to 1920x800
                processed_desktop_image = process_hero_image(desktop_image)
                hero_image.desktop_image = processed_desktop_image
                
            except ValidationError as e:
                messages.error(request, str(e))
                return render(request, 'furfeast/dashboard/hero_image_form.html', {'hero_image': hero_image})
        
        # Handle mobile image update
        if 'mobile_image' in request.FILES:
            mobile_image = request.FILES['mobile_image']
            
            # Validate file size (100KB minimum, 10MB maximum)
            if mobile_image.size < 100 * 1024:  # 100KB
                messages.error(request, 'Mobile image file must be at least 100KB in size.')
                return render(request, 'furfeast/dashboard/hero_image_form.html', {'hero_image': hero_image})
            
            if mobile_image.size > 10 * 1024 * 1024:  # 10MB
                messages.error(request, 'Mobile image file must be less than 10MB in size.')
                return render(request, 'furfeast/dashboard/hero_image_form.html', {'hero_image': hero_image})
            
            hero_image.mobile_image = mobile_image
        
        # Handle legacy image update (for backward compatibility)
        if 'image' in request.FILES:
            image = request.FILES['image']
            
            # Validate file size (100KB minimum, 10MB maximum)
            if image.size < 100 * 1024:  # 100KB
                messages.error(request, 'Image file must be at least 100KB in size.')
                return render(request, 'furfeast/dashboard/hero_image_form.html', {'hero_image': hero_image})
            
            if image.size > 10 * 1024 * 1024:  # 10MB
                messages.error(request, 'Image file must be less than 10MB in size.')
                return render(request, 'furfeast/dashboard/hero_image_form.html', {'hero_image': hero_image})
            
            try:
                # Process legacy image to 1920x800
                processed_image = process_hero_image(image)
                hero_image.image = processed_image
                
            except ValidationError as e:
                messages.error(request, str(e))
                return render(request, 'furfeast/dashboard/hero_image_form.html', {'hero_image': hero_image})
        
        hero_image.save()
        
        # Apply position to all hero images if requested
        if apply_to_all:
            HeroImage.objects.exclude(id=hero_image.id).update(
                text_position_y=hero_image.text_position_y, 
                text_position_x=hero_image.text_position_x
            )
            messages.success(request, 'Hero image updated and text position applied to all hero images.')
        else:
            messages.success(request, 'Hero image updated successfully with responsive images.')
        
        return redirect('dashboard_hero_image_list')
    
    return render(request, 'furfeast/dashboard/hero_image_form.html', {'hero_image': hero_image})

@user_passes_test(is_admin)
def hero_image_delete(request, image_id):
    hero_image = get_object_or_404(HeroImage, id=image_id)
    hero_image.delete()
    messages.success(request, 'Hero image deleted successfully.')
    return redirect('dashboard_hero_image_list')

# --- FurFeast Family Management ---

@user_passes_test(is_admin)
def furfeast_family_list(request):
    family_members = FurFeastFamily.objects.all().select_related('user').order_by('-joined_at')
    
    # Filter by pet category
    category_filter = request.GET.get('category')
    if category_filter:
        family_members = family_members.filter(pet_category=category_filter)
    
    # Filter by time period
    period_filter = request.GET.get('period')
    if period_filter:
        from datetime import datetime, timedelta
        now = timezone.now()
        
        if period_filter == 'week':
            start_date = now - timedelta(days=7)
        elif period_filter == 'month':
            start_date = now - timedelta(days=30)
        elif period_filter == '3months':
            start_date = now - timedelta(days=90)
        elif period_filter == '6months':
            start_date = now - timedelta(days=180)
        elif period_filter == 'year':
            start_date = now - timedelta(days=365)
        else:
            start_date = None
            
        if start_date:
            family_members = family_members.filter(joined_at__gte=start_date)
    
    context = {
        'family_members': family_members,
        'category_filter': category_filter,
        'period_filter': period_filter,
        'pet_categories': FurFeastFamily.PET_CATEGORY_CHOICES
    }
    return render(request, 'furfeast/dashboard/furfeast_family_list.html', context)

# --- Customer Analytics ---

@user_passes_test(is_admin)
def customer_analytics(request):
    # Get customer segments
    registered_customers = User.objects.filter(is_staff=False).count()
    customers_with_orders = User.objects.filter(is_staff=False, order__isnull=False).distinct().count()
    
    context = {
        'registered_customers': registered_customers,
        'customers_with_orders': customers_with_orders,
        'recent_campaigns': MassEmailCampaign.objects.order_by('-created_at')[:5]
    }
    return render(request, 'furfeast/dashboard/customer_analytics.html', context)

@user_passes_test(is_admin)
def send_mass_email(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        send_to_registered = request.POST.get('send_to_registered') == 'on'
        send_to_customers = request.POST.get('send_to_customers') == 'on'
        send_to_furfeast_family = request.POST.get('send_to_furfeast_family') == 'on'
        
        # Create campaign record
        campaign = MassEmailCampaign.objects.create(
            title=title,
            subject=subject,
            body=body,
            image=image,
            video=video,
            sent_to_registered=send_to_registered,
            sent_to_customers=send_to_customers,
            sent_to_furfeast_family=send_to_furfeast_family
        )
        
        # Get email lists
        emails = []
        if send_to_registered:
            emails.extend(User.objects.filter(is_staff=False).values_list('email', flat=True))
        if send_to_customers:
            emails.extend(User.objects.filter(is_staff=False, order__isnull=False).distinct().values_list('email', flat=True))
        if send_to_furfeast_family:
            emails.extend(FurFeastFamily.objects.filter(receive_expert_emails=True).values_list('user__email', flat=True))
        
        # Remove duplicates
        emails = list(set(filter(None, emails)))
        campaign.recipients_count = len(emails)
        
        # Send emails with attachments
        try:
            from django.core.mail import EmailMessage
            for email in emails:
                msg = EmailMessage(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                
                # Attach media files
                if campaign.image:
                    msg.attach_file(campaign.image.path)
                if campaign.video:
                    msg.attach_file(campaign.video.path)
                
                msg.send(fail_silently=False)
            
            campaign.sent_at = timezone.now()
            campaign.save()
            messages.success(request, f'Mass email sent to {len(emails)} recipients!')
        except Exception as e:
            messages.error(request, f'Failed to send emails: {str(e)}')
        
        return redirect('dashboard_customer_analytics')
    
    return redirect('dashboard_customer_analytics')

@user_passes_test(is_admin)
def campaign_list(request):
    campaigns = MassEmailCampaign.objects.order_by('-created_at')
    return render(request, 'furfeast/dashboard/campaign_list.html', {'campaigns': campaigns})

@user_passes_test(is_admin)
def campaign_edit(request, campaign_id):
    campaign = get_object_or_404(MassEmailCampaign, id=campaign_id)
    if campaign.sent_at:
        messages.error(request, 'Cannot edit sent campaigns.')
        return redirect('dashboard_campaign_list')
    
    if request.method == 'POST':
        campaign.title = request.POST.get('title')
        campaign.subject = request.POST.get('subject')
        campaign.body = request.POST.get('body')
        if 'image' in request.FILES:
            campaign.image = request.FILES['image']
        if 'video' in request.FILES:
            campaign.video = request.FILES['video']
        campaign.save()
        messages.success(request, 'Campaign updated successfully.')
        return redirect('dashboard_campaign_list')
    
    return render(request, 'furfeast/dashboard/campaign_form.html', {'campaign': campaign})

@user_passes_test(is_admin)
def campaign_delete(request, campaign_id):
    campaign = get_object_or_404(MassEmailCampaign, id=campaign_id)
    campaign.delete()
    messages.success(request, 'Campaign deleted successfully.')
    return redirect('dashboard_campaign_list')

@user_passes_test(is_admin)
def campaign_resend(request, campaign_id):
    campaign = get_object_or_404(MassEmailCampaign, id=campaign_id)
    
    if request.method == 'POST':
        # Get email lists
        emails = []
        if campaign.sent_to_registered:
            emails.extend(User.objects.filter(is_staff=False).values_list('email', flat=True))
        if campaign.sent_to_customers:
            emails.extend(User.objects.filter(is_staff=False, order__isnull=False).distinct().values_list('email', flat=True))
        
        # Remove duplicates
        emails = list(set(filter(None, emails)))
        
        # Send emails with attachments
        try:
            from django.core.mail import EmailMessage
            for email in emails:
                msg = EmailMessage(
                    campaign.subject,
                    campaign.body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                
                # Attach media files
                if campaign.image:
                    msg.attach_file(campaign.image.path)
                if campaign.video:
                    msg.attach_file(campaign.video.path)
                
                msg.send(fail_silently=False)
            
            # Update campaign
            campaign.sent_at = timezone.now()
            campaign.recipients_count = len(emails)
            campaign.save()
            
            messages.success(request, f'Campaign resent to {len(emails)} recipients!')
        except Exception as e:
            messages.error(request, f'Failed to resend campaign: {str(e)}')
        
        return redirect('dashboard_campaign_list')
    
    return render(request, 'furfeast/dashboard/campaign_resend.html', {'campaign': campaign})

# --- Business Analytics ---

@user_passes_test(is_admin)
def business_analytics(request):
    from django.db.models import Sum, Count
    from datetime import datetime, timedelta
    import json
    
    # Get customer data with sorting
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')
    
    customers = User.objects.filter(is_staff=False).annotate(
        total_orders=Count('order'),
        total_spent=Sum('order__total_amount')
    )
    
    # Apply sorting
    if sort_by == 'name':
        customers = customers.order_by('first_name' if order == 'asc' else '-first_name')
    elif sort_by == 'email':
        customers = customers.order_by('email' if order == 'asc' else '-email')
    elif sort_by == 'orders':
        customers = customers.order_by('total_orders' if order == 'asc' else '-total_orders')
    elif sort_by == 'spent':
        customers = customers.order_by('total_spent' if order == 'asc' else '-total_spent')
    
    # Pagination
    paginator = Paginator(customers, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    # Chart data
    now = timezone.now()
    
    # This week data
    week_start = now - timedelta(days=now.weekday())
    week_orders = Order.objects.filter(created_at__gte=week_start).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # This month data
    month_start = now.replace(day=1)
    month_orders = Order.objects.filter(created_at__gte=month_start).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # This year data
    year_start = now.replace(month=1, day=1)
    year_orders = Order.objects.filter(created_at__gte=year_start).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Get targets
    from .models import BusinessTarget
    week_target = BusinessTarget.objects.filter(period='week', year=now.year).first()
    month_target = BusinessTarget.objects.filter(period='month', year=now.year, month=now.month).first()
    year_target = BusinessTarget.objects.filter(period='year', year=now.year).first()
    
    # Calculate progress percentages
    week_progress = (float(week_orders) * 100 / float(week_target.target_amount)) if week_target and week_target.target_amount > 0 else 0
    month_progress = (float(month_orders) * 100 / float(month_target.target_amount)) if month_target and month_target.target_amount > 0 else 0
    year_progress = (float(year_orders) * 100 / float(year_target.target_amount)) if year_target and year_target.target_amount > 0 else 0
    
    context = {
        'customers': page_obj,
        'sort_by': sort_by,
        'order': order,
        'week_sales': float(week_orders),
        'month_sales': float(month_orders),
        'year_sales': float(year_orders),
        'week_target': week_target,
        'month_target': month_target,
        'year_target': year_target,
        'week_progress': min(100, week_progress),
        'month_progress': min(100, month_progress),
        'year_progress': min(100, year_progress),
    }
    
    return render(request, 'furfeast/dashboard/business_analytics.html', context)

@user_passes_test(is_admin)
def set_target(request):
    if request.method == 'POST':
        from .models import BusinessTarget
        period = request.POST.get('period')
        amount = request.POST.get('amount')
        
        now = timezone.now()
        target_data = {
            'period': period,
            'target_amount': amount,
            'year': now.year
        }
        
        if period == 'month':
            target_data['month'] = now.month
        elif period == 'week':
            target_data['week'] = now.isocalendar()[1]
        
        BusinessTarget.objects.update_or_create(
            period=period,
            year=now.year,
            month=target_data.get('month'),
            week=target_data.get('week'),
            defaults={'target_amount': amount}
        )
        
        messages.success(request, f'{period.title()} target set successfully!')
    
    return redirect('dashboard_business_analytics')

@user_passes_test(is_admin)
def delete_target(request, period):
    from .models import BusinessTarget
    now = timezone.now()
    
    filter_data = {'period': period, 'year': now.year}
    if period == 'month':
        filter_data['month'] = now.month
    elif period == 'week':
        filter_data['week'] = now.isocalendar()[1]
    
    BusinessTarget.objects.filter(**filter_data).delete()
    messages.success(request, f'{period.title()} target deleted successfully!')
    return redirect('dashboard_business_analytics')

@user_passes_test(is_admin)
def customer_queries(request):
    from datetime import timedelta
    
    # Auto-delete messages older than 1 month
    one_month_ago = timezone.now() - timedelta(days=30)
    ContactMessage.objects.filter(created_at__lt=one_month_ago).delete()
    
    # Get filter parameter
    filter_param = request.GET.get('filter', 'all')
    
    # Get all messages with user profile data
    messages_list = ContactMessage.objects.select_related('user', 'user__profile').order_by('-created_at')
    
    # Apply time filters
    now = timezone.now()
    if filter_param == 'month':
        start_date = now - timedelta(days=30)
        messages_list = messages_list.filter(created_at__gte=start_date)
    elif filter_param == 'week':
        start_date = now - timedelta(days=7)
        messages_list = messages_list.filter(created_at__gte=start_date)
    elif filter_param == '3days':
        start_date = now - timedelta(days=3)
        messages_list = messages_list.filter(created_at__gte=start_date)
    
    context = {
        'messages_list': messages_list
    }
    return render(request, 'furfeast/dashboard/customer_queries.html', context)

@user_passes_test(is_admin)
@require_POST
def clear_messages(request):
    ContactMessage.objects.all().delete()
    return JsonResponse({'success': True})

@user_passes_test(is_admin)
@require_POST
def delete_message(request, message_id):
    try:
        message = get_object_or_404(ContactMessage, id=message_id)
        message.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@user_passes_test(is_admin)
def message_count(request):
    count = ContactMessage.objects.count()
    return JsonResponse({'count': count})

@user_passes_test(is_admin)
def chat_message_count(request):
    """Count unread customer messages (not from admin)"""
    count = CustomerMessage.objects.filter(is_from_admin=False, is_read=False).count()
    return JsonResponse({'count': count})

@user_passes_test(is_admin)
def customer_messages_list(request):
    """List all customers with messages - sorted by most recent"""
    from .models import ChatRoom
    from django.db.models import Count, Q
    
    chat_rooms = ChatRoom.objects.annotate(
        unread_count=Count('messages', filter=Q(
            messages__is_read=False, 
            messages__is_from_admin=False
        ))
    ).order_by('-updated_at')
    
    customer_data = []
    for chat_room in chat_rooms:
        last_msg = chat_room.messages.order_by('-created_at').first()
        customer_data.append({
            'user': chat_room.customer,
            'chat_room_id': chat_room.id,
            'last_message': last_msg.message[:50] if last_msg and last_msg.message else ('📷 Image' if last_msg else 'No messages yet'),
            'last_message_time': last_msg.created_at if last_msg else chat_room.created_at,
            'last_message_from_admin': last_msg.is_from_admin if last_msg else False,
            'unread_count': chat_room.unread_count,
            'has_unread': chat_room.has_unread_messages
        })
    
    return render(request, 'furfeast/dashboard/customer_messages_list.html', {'customers': customer_data})

@user_passes_test(is_admin)
@never_cache
def customer_chat_detail(request, user_id):
    """Chat with specific customer - loads messages from DB on page load"""
    from .models import ChatRoom
    customer = get_object_or_404(User, id=user_id)
    chat_room, _ = ChatRoom.objects.get_or_create(customer=customer)
    chat_messages = chat_room.messages.all()
    chat_room.messages.filter(is_from_admin=False, is_read=False).update(is_read=True)
    
    response = render(request, 'furfeast/dashboard/customer_chat_detail.html', {
        'customer': customer,
        'chat_room': chat_room,
        'chat_messages': chat_messages
    })
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
