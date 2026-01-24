#!/usr/bin/env python
"""
Check Google Cloud database tables and their contents
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

def check_database_connection():
    """Check current database connection"""
    print("CHECKING DATABASE CONNECTION")
    print("=" * 50)
    
    try:
        from django.db import connection
        db_settings = connection.settings_dict
        
        print(f"Database Engine: {db_settings['ENGINE']}")
        print(f"Database Name: {db_settings['NAME']}")
        print(f"Database Host: {db_settings['HOST']}")
        print(f"Database User: {db_settings['USER']}")
        print(f"Database Port: {db_settings['PORT']}")
        
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"Connected Successfully: {version[0]}")
            return True
            
    except Exception as e:
        print(f"Connection Failed: {e}")
        return False

def check_all_tables():
    """Check all tables and their data"""
    print("\nCHECKING ALL TABLES")
    print("=" * 50)
    
    try:
        from django.db import connection
        
        # Get all table names
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
        print(f"Found {len(tables)} tables:")
        for table in tables:
            table_name = table[0]
            
            # Get row count for each table
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                
            print(f"  - {table_name}: {count} rows")
            
        return tables
        
    except Exception as e:
        print(f"Error checking tables: {e}")
        return []

def check_user_data():
    """Check user-related data"""
    print("\nUSER DATA")
    print("=" * 30)
    
    try:
        from django.contrib.auth.models import User
        from furfeast.models import UserProfile
        
        users = User.objects.all()
        print(f"Total Users: {users.count()}")
        
        if users.exists():
            print("Recent Users:")
            for user in users.order_by('-date_joined')[:5]:
                profile = getattr(user, 'profile', None)
                phone = profile.phone_number if profile else 'No profile'
                print(f"  - {user.username} ({user.email}) - Phone: {phone}")
        
        profiles = UserProfile.objects.all()
        print(f"User Profiles: {profiles.count()}")
        
    except Exception as e:
        print(f"Error checking user data: {e}")

def check_product_data():
    """Check product-related data"""
    print("\nPRODUCT DATA")
    print("=" * 30)
    
    try:
        from furfeast.models import Product, Review
        
        products = Product.objects.all()
        print(f"Total Products: {products.count()}")
        
        if products.exists():
            print("Recent Products:")
            for product in products.order_by('-created_at')[:5]:
                print(f"  - {product.name} (${product.price}) - {product.category}")
        
        reviews = Review.objects.all()
        print(f"Total Reviews: {reviews.count()}")
        
        # Check categories
        categories = Product.objects.values_list('category', flat=True).distinct()
        print(f"Categories: {list(categories)}")
        
    except Exception as e:
        print(f"Error checking product data: {e}")

def check_order_data():
    """Check order-related data"""
    print("\nORDER DATA")
    print("=" * 30)
    
    try:
        from furfeast.models import Order, OrderItem, Cart, CartItem
        
        orders = Order.objects.all()
        print(f"Total Orders: {orders.count()}")
        
        if orders.exists():
            print("Recent Orders:")
            for order in orders.order_by('-created_at')[:5]:
                print(f"  - {order.order_id} - {order.user.username} - ${order.total_amount} - {order.status}")
        
        order_items = OrderItem.objects.all()
        print(f"Order Items: {order_items.count()}")
        
        carts = Cart.objects.all()
        print(f"Active Carts: {carts.count()}")
        
        cart_items = CartItem.objects.all()
        print(f"Cart Items: {cart_items.count()}")
        
    except Exception as e:
        print(f"Error checking order data: {e}")

def check_chat_data():
    """Check chat and communication data"""
    print("\nCHAT & COMMUNICATION DATA")
    print("=" * 30)
    
    try:
        from furfeast.models import (
            ChatRoom, CustomerMessage, ContactMessage, 
            Notification, ChatBotSession, ChatBotConversation
        )
        
        chat_rooms = ChatRoom.objects.all()
        print(f"Chat Rooms: {chat_rooms.count()}")
        
        messages = CustomerMessage.objects.all()
        print(f"Customer Messages: {messages.count()}")
        
        contact_msgs = ContactMessage.objects.all()
        print(f"Contact Messages: {contact_msgs.count()}")
        
        notifications = Notification.objects.all()
        print(f"Notifications: {notifications.count()}")
        
        bot_sessions = ChatBotSession.objects.all()
        print(f"Chatbot Sessions: {bot_sessions.count()}")
        
        bot_conversations = ChatBotConversation.objects.all()
        print(f"Chatbot Conversations: {bot_conversations.count()}")
        
    except Exception as e:
        print(f"Error checking chat data: {e}")

def check_marketing_data():
    """Check marketing and content data"""
    print("\nMARKETING & CONTENT DATA")
    print("=" * 30)
    
    try:
        from furfeast.models import (
            FlashSale, PromoCode, Blog, AboutUs, HeroImage,
            MassEmailCampaign, BusinessTarget, FurFeastFamily
        )
        
        flash_sales = FlashSale.objects.all()
        print(f"Flash Sales: {flash_sales.count()}")
        
        promo_codes = PromoCode.objects.all()
        print(f"Promo Codes: {promo_codes.count()}")
        
        blogs = Blog.objects.all()
        print(f"Blog Posts: {blogs.count()}")
        
        hero_images = HeroImage.objects.all()
        print(f"Hero Images: {hero_images.count()}")
        
        email_campaigns = MassEmailCampaign.objects.all()
        print(f"Email Campaigns: {email_campaigns.count()}")
        
        family_members = FurFeastFamily.objects.all()
        print(f"FurFeast Family Members: {family_members.count()}")
        
    except Exception as e:
        print(f"Error checking marketing data: {e}")

def check_wishlist_data():
    """Check wishlist data"""
    print("\nWISHLIST DATA")
    print("=" * 30)
    
    try:
        from furfeast.models import Wishlist
        
        wishlists = Wishlist.objects.all()
        print(f"Wishlist Items: {wishlists.count()}")
        
        if wishlists.exists():
            print("Recent Wishlist Items:")
            for item in wishlists.order_by('-added_at')[:5]:
                print(f"  - {item.user.username} - {item.product.name}")
        
    except Exception as e:
        print(f"Error checking wishlist data: {e}")

def main():
    """Run all checks"""
    print("GOOGLE CLOUD DATABASE CONTENT CHECK")
    print("=" * 60)
    
    # Check connection first
    if not check_database_connection():
        print("\nCannot connect to database. Please check your configuration.")
        return
    
    # Check all tables
    tables = check_all_tables()
    
    # Check specific data
    check_user_data()
    check_product_data()
    check_order_data()
    check_chat_data()
    check_marketing_data()
    check_wishlist_data()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("- If tables show 0 rows, you need to migrate data")
    print("- If connection fails, update .env with real Google Cloud credentials")
    print("- All data should be in Google Cloud SQL, not local SQLite")

if __name__ == "__main__":
    main()