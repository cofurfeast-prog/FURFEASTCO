#!/usr/bin/env python
"""
Show existing data from SQLite database (your current data)
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')

# Setup Django
django.setup()

# Override database to use SQLite temporarily
from django.conf import settings
settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': project_dir / 'db.sqlite3',
}

# Force Django to use new database settings
from django.db import connections
connections.databases = settings.DATABASES

def show_existing_data():
    """Show all existing data from SQLite"""
    print("YOUR EXISTING DATA (Currently in SQLite)")
    print("=" * 60)
    
    try:
        from django.contrib.auth.models import User
        from furfeast.models import *
        
        # Users
        users = User.objects.all()
        print(f"USERS: {users.count()}")
        for user in users[:10]:
            try:
                profile = user.profile
                phone = profile.phone_number or 'No phone'
            except:
                phone = 'No profile'
            print(f"  - {user.username} ({user.email}) - {user.first_name} {user.last_name} - {phone}")
        
        # Products
        products = Product.objects.all()
        print(f"\nPRODUCTS: {products.count()}")
        for product in products[:10]:
            print(f"  - {product.name} (${product.price}) - {product.category} - Stock: {product.stock}")
        
        # Orders
        orders = Order.objects.all()
        print(f"\nORDERS: {orders.count()}")
        for order in orders[:10]:
            print(f"  - {order.order_id} - {order.user.username} - ${order.total_amount} - {order.status}")
        
        # Reviews
        reviews = Review.objects.all()
        print(f"\nREVIEWS: {reviews.count()}")
        for review in reviews[:5]:
            print(f"  - {review.user.username} rated {review.product.name}: {review.rating}/5")
        
        # Cart Items
        cart_items = CartItem.objects.all()
        print(f"\nCART ITEMS: {cart_items.count()}")
        for item in cart_items[:5]:
            user = item.cart.user.username if item.cart.user else 'Guest'
            print(f"  - {user}: {item.quantity}x {item.product.name}")
        
        # Wishlist
        wishlists = Wishlist.objects.all()
        print(f"\nWISHLIST ITEMS: {wishlists.count()}")
        for item in wishlists[:5]:
            print(f"  - {item.user.username} wants {item.product.name}")
        
        # Chat Messages
        try:
            messages = CustomerMessage.objects.all()
            print(f"\nCHAT MESSAGES: {messages.count()}")
            for msg in messages[:3]:
                sender = 'Admin' if msg.is_from_admin else msg.chat_room.customer.username
                print(f"  - {sender}: {msg.message[:50]}...")
        except:
            print(f"\nCHAT MESSAGES: 0")
        
        # Notifications
        try:
            notifications = Notification.objects.all()
            print(f"\nNOTIFICATIONS: {notifications.count()}")
            for notif in notifications[:3]:
                print(f"  - {notif.user.username}: {notif.title}")
        except:
            print(f"\nNOTIFICATIONS: 0")
        
        # Flash Sales
        try:
            flash_sales = FlashSale.objects.all()
            print(f"\nFLASH SALES: {flash_sales.count()}")
            for sale in flash_sales[:3]:
                print(f"  - {sale.discount_percentage}% off - {sale.title or 'Untitled'}")
        except:
            print(f"\nFLASH SALES: 0")
        
        # Promo Codes
        try:
            promos = PromoCode.objects.all()
            print(f"\nPROMO CODES: {promos.count()}")
            for promo in promos[:3]:
                print(f"  - {promo.code}: ${promo.discount_amount} off")
        except:
            print(f"\nPROMO CODES: 0")
        
        # Blog Posts
        try:
            blogs = Blog.objects.all()
            print(f"\nBLOG POSTS: {blogs.count()}")
            for blog in blogs[:3]:
                print(f"  - {blog.title} by {blog.author.username}")
        except:
            print(f"\nBLOG POSTS: 0")
        
        # FurFeast Family
        try:
            family = FurFeastFamily.objects.all()
            print(f"\nFURFEAST FAMILY MEMBERS: {family.count()}")
            for member in family[:3]:
                print(f"  - {member.user.username}: {member.pet_name} ({member.pet_category})")
        except:
            print(f"\nFURFEAST FAMILY MEMBERS: 0")
        
        print(f"\n" + "=" * 60)
        print("STATUS: This is your existing data in SQLite")
        print("TO MIGRATE TO GOOGLE CLOUD:")
        print("1. Set up Google Cloud SQL instance")
        print("2. Update .env with real Google Cloud credentials")
        print("3. Run: python manage.py migrate")
        print("4. Export this data and import to Google Cloud")
        
    except Exception as e:
        print(f"Error reading data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    show_existing_data()