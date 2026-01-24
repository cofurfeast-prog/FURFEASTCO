import re
import uuid
from django.utils import timezone
from .models import ChatBotIntent, ChatBotSession, ChatBotConversation, Product, Order, User

class FurFeastChatBot:
    def __init__(self):
        self.default_responses = {
            'greeting': "Hello! I'm FurFeast Bot 🐾 How can I help you today?\n\nI can help you with:\n• Product information & pricing\n• Inventory & categories\n• Payment methods & shipping\n• Contact & social media info\n• Order tracking\n\nJust ask me anything!",
            'fallback': "I'm sorry, I didn't understand that. You can ask me about:\n\n🛍️ Products & inventory\n💰 Pricing & payment methods\n📍 Shop location & delivery\n📱 Social media & contact info\n📦 Order tracking\n\nTry asking something like 'What products do you have?' or 'How can I pay?'",
            'goodbye': "Thank you for visiting FurFeast! Have a pawsome day! 🐕🐱\n\nDon't forget to:\n• Follow us on social media\n• Check out our latest products\n• Contact us if you need help\n\nSee you soon! 🐾"
        }
    
    def get_or_create_session(self, user=None, session_id=None):
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session, created = ChatBotSession.objects.get_or_create(
            session_id=session_id,
            defaults={'user': user}
        )
        return session
    
    def process_message(self, message, user=None, session_id=None):
        session = self.get_or_create_session(user, session_id)
        
        # Clean and normalize message
        clean_message = message.lower().strip()
        
        # Find matching intent
        intent, response = self.match_intent(clean_message, user, session)
        
        # Save conversation
        ChatBotConversation.objects.create(
            session=session,
            user_message=message,
            bot_response=response,
            intent_matched=intent
        )
        
        # Update session context
        session.last_intent = intent
        session.updated_at = timezone.now()
        session.save()
        
        return {
            'response': response,
            'intent': intent,
            'session_id': session.session_id
        }
    
    def match_intent(self, message, user=None, session=None):
        # Check for greetings
        if any(word in message for word in ['hello', 'hi', 'hey', 'start']):
            return 'greeting', self.default_responses['greeting']
        
        # Check for goodbye
        if any(word in message for word in ['bye', 'goodbye', 'thanks', 'thank you']):
            return 'goodbye', self.default_responses['goodbye']
        
        # Help queries
        if any(word in message for word in ['help', 'what can you do', 'options', 'menu']):
            return 'help', self.get_help_info()
        
        # Inventory/Stock queries
        if any(word in message for word in ['inventory', 'stock', 'available', 'in stock', 'what products', 'what do you have']):
            return 'inventory', self.get_inventory_info()
        
        # Product categories
        if any(word in message for word in ['categories', 'types', 'what kind', 'product types']):
            return 'categories', self.get_categories_info()
        
        # Specific product search
        if any(word in message for word in ['search', 'find', 'looking for']):
            return 'search', self.get_search_help()
        
        # Product queries
        if any(word in message for word in ['dog food', 'dog', 'puppy']):
            return 'dog_food', self.get_dog_food_info()
        
        if any(word in message for word in ['cat food', 'cat', 'kitten']):
            return 'cat_food', self.get_cat_food_info()
        
        if any(word in message for word in ['accessories', 'toy', 'collar', 'leash']):
            return 'accessories', self.get_accessories_info()
        
        # Payment methods
        if any(word in message for word in ['payment', 'pay', 'payment method', 'how to pay', 'paypal', 'cod', 'cash on delivery']):
            return 'payment', self.get_payment_info()
        
        # Shop location
        if any(word in message for word in ['location', 'address', 'where', 'shop location', 'store']):
            return 'location', self.get_location_info()
        
        # Social media
        if any(word in message for word in ['facebook', 'instagram', 'tiktok', 'social media', 'follow']):
            return 'social', self.get_social_media_info()
        
        # Order queries
        if user and any(word in message for word in ['order', 'my order', 'track']):
            return 'order_status', self.get_order_status(user)
        
        # Shipping info
        if any(word in message for word in ['shipping', 'delivery', 'ship']):
            return 'shipping', self.get_shipping_info()
        
        # Contact info
        if any(word in message for word in ['contact', 'phone', 'email', 'call']):
            return 'contact', self.get_contact_info()
        
        # About company
        if any(word in message for word in ['about', 'company', 'furfeast']):
            return 'about', self.get_about_info()
        
        # Price queries
        if any(word in message for word in ['price', 'cost', 'cheap', 'expensive']):
            return 'pricing', self.get_pricing_info()
        
        # Check database intents
        intents = ChatBotIntent.objects.filter(is_active=True).order_by('-priority')
        for intent in intents:
            if any(keyword.lower() in message for keyword in intent.keywords):
                return intent.name, intent.response_template
        
        return 'fallback', self.default_responses['fallback']
    
    def get_dog_food_info(self):
        try:
            products = Product.objects.filter(category='dog-food', is_out_of_stock=False)[:5]
            count = products.count()
            
            if count == 0:
                return "We're currently updating our dog food selection. Please check back soon!"
            
            response = f"🐕 **Dog Food Collection** ({count} products available)\n\n"
            
            for product in products:
                price_info = f"Rs. {product.price}"
                if product.original_price and product.original_price > product.price:
                    price_info = f"Rs. {product.price} (was Rs. {product.original_price})"
                response += f"• **{product.name}** - {price_info}\n"
            
            response += f"\n🛒 Visit our Dog Food section to see all {Product.objects.filter(category='dog-food').count()} options and place your order!"
            return response
        except:
            return "🐕 We have a great selection of dog food! Visit our Dog Food section to see all available options."
    
    def get_cat_food_info(self):
        try:
            products = Product.objects.filter(category='cat-food', is_out_of_stock=False)[:5]
            count = products.count()
            
            if count == 0:
                return "We're currently updating our cat food selection. Please check back soon!"
            
            response = f"🐱 **Cat Food Collection** ({count} products available)\n\n"
            
            for product in products:
                price_info = f"Rs. {product.price}"
                if product.original_price and product.original_price > product.price:
                    price_info = f"Rs. {product.price} (was Rs. {product.original_price})"
                response += f"• **{product.name}** - {price_info}\n"
            
            response += f"\n🛒 Visit our Cat Food section to see all {Product.objects.filter(category='cat-food').count()} options and place your order!"
            return response
        except:
            return "🐱 We have a great selection of cat food! Visit our Cat Food section to see all available options."
    
    def get_accessories_info(self):
        try:
            products = Product.objects.filter(category='accessories', is_out_of_stock=False)[:5]
            count = products.count()
            
            if count == 0:
                return "We're currently updating our accessories selection. Please check back soon!"
            
            response = f"🎾 **Pet Accessories** ({count} products available)\n\n"
            
            for product in products:
                price_info = f"Rs. {product.price}"
                if product.original_price and product.original_price > product.price:
                    price_info = f"Rs. {product.price} (was Rs. {product.original_price})"
                response += f"• **{product.name}** - {price_info}\n"
            
            response += f"\n🛒 Check out our Accessories section to see all {Product.objects.filter(category='accessories').count()} items!"
            return response
        except:
            return "🎾 We have amazing pet accessories! Check out our Accessories section for toys, collars, and more."
    
    def get_order_status(self, user):
        recent_order = Order.objects.filter(user=user).order_by('-created_at').first()
        
        if not recent_order:
            return "You don't have any orders yet. Start shopping to place your first order! 🛒"
        
        status_messages = {
            'pending': 'is being processed',
            'paid': 'has been confirmed and is being prepared',
            'processing': 'is being prepared for shipment',
            'shipped': f'has been shipped with tracking number {recent_order.tracking_number or "TBD"}',
            'delivered': 'has been delivered successfully',
            'cancelled': 'has been cancelled'
        }
        
        status_msg = status_messages.get(recent_order.status, 'is being processed')
        return f"Your recent order {recent_order.order_id} {status_msg}. Total: Rs. {recent_order.total_amount}"
    
    def get_shipping_info(self):
        return """🚚 Shipping Information:
• Free shipping on orders above Rs. 500
• Delivery within 2-5 business days in Kathmandu Valley
• 5-7 business days for other areas
• We use reliable courier services like DHL and local partners
• You'll receive tracking information once your order ships"""
    
    def get_contact_info(self):
        return """📞 Contact FurFeast:

📧 **Email:** cofurfeast@gmail.com
• We respond within 24 hours
• For orders, complaints, or general inquiries

💬 **Live Chat:** Available on our website
• Instant customer support
• Real-time assistance

📱 **Social Media:**
• Facebook: FurFeast Nepal
• Instagram: @furfeast_nepal  
• TikTok: @furfeastco

🕒 **Response Time:**
• Chat: Instant during business hours
• Email: Within 24 hours
• Social media: 1-2 hours

We're here to help you and your furry friends! 🐾"""
    
    def get_about_info(self):
        return """🐾 About FurFeast:
We're Nepal's premium pet food company, dedicated to providing high-quality nutrition for your furry friends. We offer:
• Premium dog and cat food from trusted brands
• Pet accessories and toys
• Fast delivery across Nepal
• Expert customer support
• 10k+ happy pet parents trust us!"""
    
    def get_pricing_info(self):
        return """💰 Our Pricing:
• Dog food: Starting from Rs. 200
• Cat food: Starting from Rs. 180
• Accessories: Starting from Rs. 50
• Free shipping on orders above Rs. 500
• Regular discounts and flash sales
• Best prices guaranteed in Nepal!"""
    
    def get_inventory_info(self):
        """Get current inventory information"""
        try:
            dog_count = Product.objects.filter(category='dog-food', is_out_of_stock=False).count()
            cat_count = Product.objects.filter(category='cat-food', is_out_of_stock=False).count()
            acc_count = Product.objects.filter(category='accessories', is_out_of_stock=False).count()
            total_count = dog_count + cat_count + acc_count
            
            return f"""📦 Current Inventory:
• {dog_count} Dog food products in stock
• {cat_count} Cat food products in stock  
• {acc_count} Pet accessories in stock
• Total: {total_count} products available

All products are fresh and ready for delivery! Visit our shop to see the full collection."""
        except:
            return "📦 We have a wide range of pet products in stock! Visit our shop to see all available items."
    
    def get_categories_info(self):
        """Get product categories information"""
        return """🏷️ Our Product Categories:

🐕 **Dog Food**
• Premium dry food
• Wet food & treats
• Puppy special formulas
• Adult & senior dog nutrition

🐱 **Cat Food**
• High-quality dry food
• Wet food & treats
• Kitten special formulas
• Adult & senior cat nutrition

🎾 **Pet Accessories**
• Toys & entertainment
• Collars & leashes
• Feeding bowls
• Grooming supplies

Browse our shop to see all products in each category!"""
    
    def get_payment_info(self):
        """Get payment methods information"""
        return """💳 Payment Methods We Accept:

✅ **PayPal**
• Secure international payments
• Credit/Debit cards via PayPal
• Instant payment confirmation

✅ **Cash on Delivery (COD)**
• Pay when you receive your order
• Available across Nepal
• No advance payment required

🔒 All payments are 100% secure and encrypted. Choose the method that's most convenient for you!"""
    
    def get_location_info(self):
        """Get shop location information"""
        return """📍 FurFeast Shop Location:

🏪 **Online Store**
We operate as an online pet store serving all of Nepal!

🚚 **Delivery Areas:**
• Kathmandu Valley: 2-3 days
• Major cities: 3-5 days
• Remote areas: 5-7 days

📧 **Contact Us:**
• Email: cofurfeast@gmail.com
• We deliver right to your doorstep!

No physical store visits needed - shop online and we'll bring everything to you! 🐾"""
    
    def get_social_media_info(self):
        """Get social media and contact information"""
        return """📱 Follow FurFeast Online:

🔗 **Social Media:**
• Facebook: Search "FurFeast Nepal" 
• Instagram: @furfeast_nepal
• TikTok: @furfeastco

📞 **Contact Methods:**
• Email: cofurfeast@gmail.com
• Website: Browse our online store
• Customer Chat: Use the chat feature on our website

💬 Follow us for:
• Pet care tips
• New product updates
• Special offers & discounts
• Happy customer stories

Stay connected with the FurFeast family! 🐾❤️"""
    
    def get_help_info(self):
        """Get help information about what the bot can do"""
        return """🤖 **FurFeast Bot Help Menu**

I can help you with:

🛍️ **Products & Shopping:**
• "What products do you have?"
• "Show me dog food"
• "Cat food prices"
• "Pet accessories"

💰 **Pricing & Payments:**
• "How much does it cost?"
• "Payment methods"
• "Do you accept PayPal?"

🚚 **Delivery & Location:**
• "Where is your shop?"
• "Shipping information"
• "Delivery time"

📱 **Contact & Social:**
• "How to contact you?"
• "Social media links"
• "Facebook page"

📦 **Orders:**
• "Track my order"
• "Order status"

Just type your question naturally! 😊"""
    
    def get_search_help(self):
        """Help users with product search"""
        return """🔍 **Product Search Help:**

Tell me what you're looking for:
• "I need dog food for puppies"
• "Show me cat toys"
• "Looking for pet collars"
• "What's the cheapest dog food?"

Or browse by category:
• Dog Food - Premium nutrition for dogs
• Cat Food - Quality meals for cats  
• Accessories - Toys, collars, bowls & more

You can also use the search bar on our website to find specific products! 🛍️"""

# Initialize chatbot instance
chatbot = FurFeastChatBot()