from django.urls import path
from . import views, dashboard_views, api_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('health/', views.health_check, name='health_check'),  # Health check endpoint
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('product/<int:product_id>/buy-now/', views.buy_now, name='buy_now'),
    path('shop/', views.shop, name='shop'),
    path('dog-food/', views.dog_food, name='dog_food'),
    path('cat-food/', views.cat_food, name='cat_food'),
    path('accessories/', views.accessories, name='accessories'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('cart/', views.cart_view, name='cart'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('shipping/', views.shipping, name='shipping'),
    path('refund/', views.refund, name='refund'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    
    # APIs
    path('api/cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('api/cart/clear/', views.clear_cart, name='clear_cart'),
    path('api/wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('api/wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('api/wishlist/clear/', views.clear_wishlist, name='clear_wishlist'),
    path('api/paypal/capture/', views.paypal_capture, name='paypal_capture'),
    path('api/cod/order/', views.cod_order, name='cod_order'),
    path('api/notifications/', views.notifications_api, name='get_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/clear/', views.clear_all_notifications, name='clear_all_notifications'),
    path('test-notification/', views.test_notification, name='test_notification'),
    path('test-notification-api/', views.test_notification_api, name='test_notification_api'),
    
    # User
    path('profile/', views.profile_view, name='profile'),
    path('profile/upload-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('profile/delete-picture/', views.delete_profile_picture, name='delete_profile_picture'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('order-tracking/<str:order_id>/', views.order_tracking, name='order_tracking'),
    path('search/', views.search_products, name='search_products'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('order-success/', views.order_success, name='order_success'),
    path('join-furfeast-family/', views.join_furfeast_family, name='join_furfeast_family'),
    path('furfeast-family-form/', views.furfeast_family_form, name='furfeast_family_form'),

    # Admin Dashboard
    path('dashboard/', dashboard_views.dashboard_home, name='dashboard_home'),
    
    # Products
    path('dashboard/products/', dashboard_views.product_list, name='dashboard_product_list'),
    path('dashboard/products/create/', dashboard_views.product_create, name='dashboard_product_create'),
    path('dashboard/products/<int:product_id>/edit/', dashboard_views.product_edit, name='dashboard_product_edit'),
    path('dashboard/products/<int:product_id>/delete/', dashboard_views.product_delete, name='dashboard_product_delete'),
    
    # Orders
    path('dashboard/orders/', dashboard_views.order_list, name='dashboard_order_list'),
    path('dashboard/orders/<int:order_id>/', dashboard_views.order_detail, name='dashboard_order_detail'),
    path('dashboard/orders/<int:order_id>/update-status/', dashboard_views.order_update_status, name='dashboard_order_update_status'),
    path('admin/update-order-status/', dashboard_views.update_order_status_ajax, name='update_order_status_ajax'),
    
    # Flash Sales
    path('dashboard/flash-sales/', dashboard_views.flash_sale_list, name='dashboard_flash_sale_list'),
    path('dashboard/flash-sales/create/', dashboard_views.flash_sale_create, name='dashboard_flash_sale_create'),
    path('dashboard/flash-sales/<int:sale_id>/edit/', dashboard_views.flash_sale_edit, name='dashboard_flash_sale_edit'),
    path('dashboard/flash-sales/<int:sale_id>/delete/', dashboard_views.flash_sale_delete, name='dashboard_flash_sale_delete'),
    
    # Promo Codes
    path('dashboard/promo-codes/', dashboard_views.promo_code_list, name='dashboard_promo_code_list'),
    path('dashboard/promo-codes/create/', dashboard_views.promo_code_create, name='dashboard_promo_code_create'),
    path('dashboard/promo-codes/<int:code_id>/edit/', dashboard_views.promo_code_edit, name='dashboard_promo_code_edit'),
    path('dashboard/promo-codes/<int:code_id>/delete/', dashboard_views.promo_code_delete, name='dashboard_promo_code_delete'),
    
    # Blogs
    path('dashboard/blogs/', dashboard_views.blog_list, name='dashboard_blog_list'),
    path('dashboard/blogs/create/', dashboard_views.blog_create, name='dashboard_blog_create'),
    path('dashboard/blogs/<int:blog_id>/edit/', dashboard_views.blog_edit, name='dashboard_blog_edit'),
    path('dashboard/blogs/<int:blog_id>/delete/', dashboard_views.blog_delete, name='dashboard_blog_delete'),
    
    # Admins
    path('dashboard/admins/', dashboard_views.admin_list, name='dashboard_admin_list'),
    path('dashboard/admins/create/', dashboard_views.admin_create, name='dashboard_admin_create'),
    path('dashboard/admins/<int:admin_id>/edit/', dashboard_views.admin_edit, name='dashboard_admin_edit'),
    path('dashboard/admins/<int:admin_id>/delete/', dashboard_views.admin_delete, name='dashboard_admin_delete'),
    
    # About Us
    path('dashboard/about-us/', dashboard_views.about_us_edit, name='dashboard_about_us_edit'),
    
    # Hero Images
    path('dashboard/hero-images/', dashboard_views.hero_image_list, name='dashboard_hero_image_list'),
    path('dashboard/hero-images/create/', dashboard_views.hero_image_create, name='dashboard_hero_image_create'),
    path('dashboard/hero-images/<int:image_id>/edit/', dashboard_views.hero_image_edit, name='dashboard_hero_image_edit'),
    path('dashboard/hero-images/<int:image_id>/delete/', dashboard_views.hero_image_delete, name='dashboard_hero_image_delete'),
    
    # FurFeast Family
    path('dashboard/furfeast-family/', dashboard_views.furfeast_family_list, name='dashboard_furfeast_family_list'),
    
    # Customer Analytics
    path('dashboard/customer-analytics/', dashboard_views.customer_analytics, name='dashboard_customer_analytics'),
    path('dashboard/send-mass-email/', dashboard_views.send_mass_email, name='dashboard_send_mass_email'),
    path('dashboard/campaigns/', dashboard_views.campaign_list, name='dashboard_campaign_list'),
    path('dashboard/campaigns/<int:campaign_id>/edit/', dashboard_views.campaign_edit, name='dashboard_campaign_edit'),
    path('dashboard/campaigns/<int:campaign_id>/delete/', dashboard_views.campaign_delete, name='dashboard_campaign_delete'),
    path('dashboard/campaigns/<int:campaign_id>/resend/', dashboard_views.campaign_resend, name='dashboard_campaign_resend'),
    
    # Business Analytics
    path('dashboard/business-analytics/', dashboard_views.business_analytics, name='dashboard_business_analytics'),
    path('dashboard/set-target/', dashboard_views.set_target, name='dashboard_set_target'),
    path('dashboard/delete-target/<str:period>/', dashboard_views.delete_target, name='dashboard_delete_target'),
    
    # Customer Queries
    path('dashboard/customer-queries/', dashboard_views.customer_queries, name='dashboard_customer_queries'),
    path('dashboard/clear-messages/', dashboard_views.clear_messages, name='dashboard_clear_messages'),
    path('dashboard/delete-message/<int:message_id>/', dashboard_views.delete_message, name='dashboard_delete_message'),
    path('dashboard/message-count/', dashboard_views.message_count, name='dashboard_message_count'),
    path('dashboard/chat-message-count/', dashboard_views.chat_message_count, name='dashboard_chat_message_count'),
    
    # Customer Chat Messages (Chat)
    path('dashboard/customer-messages/', dashboard_views.customer_messages_list, name='dashboard_customer_messages_list'),
    path('dashboard/customer-messages/<int:user_id>/', dashboard_views.customer_chat_detail, name='dashboard_customer_chat_detail'),
    
    # Customer Chat (Frontend)
    path('chat/', views.customer_chat, name='customer_chat'),
    path('api/chat/send/', views.send_customer_message, name='send_customer_message'),
    path('api/chat/messages/', views.get_customer_messages, name='get_customer_messages'),
    path('api/chat/unread-count/', views.customer_unread_message_count, name='customer_unread_message_count'),
    path('api/chat/test/', lambda request: __import__('furfeast.test_chat', fromlist=['test_chat_messages']).test_chat_messages(request), name='test_chat_messages'),
    
    # Chatbot
    path('chatbot/', views.chatbot_widget, name='chatbot_widget'),
    path('api/chatbot/message/', views.chatbot_message, name='chatbot_message'),
    path('api/chatbot/history/<str:session_id>/', views.chatbot_history, name='chatbot_history'),
    
    # Chatbot Testing
    path('chatbot/test/', views.chatbot_test_view, name='chatbot_test'),
    path('api/chatbot/test/message/', views.chatbot_test_message, name='chatbot_test_message'),
]

# Serve static and media files in production
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# WhatsApp-style Chat API
urlpatterns += [
    path('api/chat-messages/', api_views.get_chat_messages, name='api_get_chat_messages'),
    path('api/chat-messages/<int:customer_id>/', api_views.get_chat_messages, name='api_get_chat_messages_customer'),
    path('api/send-customer-message/', api_views.api_send_customer_message, name='api_send_customer_message'),
    path('api/send-admin-message/', api_views.api_send_admin_message, name='api_send_admin_message'),
]