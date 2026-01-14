# 🐾 FurFeast Co. - Pet Food E-Commerce Platform

A full-featured Django-based e-commerce platform for pet food and accessories with real-time chat, notifications, and comprehensive admin dashboard.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Key Features Explained](#key-features-explained)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)

## ✨ Features

### Customer Features
- **Product Browsing**: Browse dog food, cat food, and accessories
- **Shopping Cart**: Add/remove items, update quantities
- **Wishlist**: Save favorite products
- **User Authentication**: Register, login, email verification, password reset
- **Profile Management**: Update profile, upload profile picture
- **Order Management**: Place orders, track status, view history
- **Real-time Chat**: Chat with admin support with typing indicators
- **Notifications**: Real-time order updates and message notifications
- **Reviews & Ratings**: Leave product reviews
- **Blog**: Read pet care articles
- **FurFeast Family**: Join community with pet details

### Admin Features
- **Dashboard**: Sales analytics, revenue tracking, customer insights
- **Product Management**: CRUD operations for products
- **Order Management**: Update order status, tracking numbers
- **Customer Chat**: Real-time messaging with customers
- **Notification System**: Automated order status notifications
- **Blog Management**: Create/edit blog posts
- **Flash Sales**: Create time-limited discounts
- **Promo Codes**: Generate discount codes
- **Email Campaigns**: Send mass emails to customers
- **Business Analytics**: Revenue charts, customer analytics
- **Hero Image Management**: Manage homepage sliders

## 🛠 Tech Stack

### Backend
- **Django 5.1.4**: Web framework
- **Django Channels**: WebSocket support for real-time features
- **Daphne**: ASGI server
- **PostgreSQL**: Database (production)
- **SQLite**: Database (development)

### Frontend
- **TailwindCSS**: Utility-first CSS framework
- **JavaScript**: Vanilla JS for interactivity
- **WebSocket**: Real-time communication

### Storage & Services
- **Supabase**: File storage for images
- **PayPal**: Payment gateway integration

### Deployment
- **Docker**: Containerization
- **Defang**: Deployment platform

## 📁 Project Structure

```
FURFEASTCO/
├── FURFEASTCO/              # Project settings
│   ├── settings.py          # Main settings
│   ├── production.py        # Production settings
│   ├── urls.py              # Root URL configuration
│   ├── asgi.py              # ASGI configuration
│   └── wsgi.py              # WSGI configuration
│
├── furfeast/                # Main application
│   ├── models.py            # Database models
│   ├── views.py             # Customer views
│   ├── dashboard_views.py   # Admin views
│   ├── consumers.py         # WebSocket consumers
│   ├── urls.py              # URL routing
│   ├── storage.py           # Supabase storage backend
│   ├── signals.py           # Django signals
│   │
│   ├── templates/           # HTML templates
│   │   └── furfeast/
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── shop.html
│   │       ├── customer_chat.html
│   │       └── dashboard/   # Admin templates
│   │
│   ├── static/              # Static files
│   │   ├── css/
│   │   └── js/
│   │       ├── components.js    # Notification system
│   │       ├── main.js          # Main JS logic
│   │       └── slider.js        # Image sliders
│   │
│   └── management/          # Custom commands
│       └── commands/
│
├── requirements.txt         # Python dependencies
├── package.json            # Node.js dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
└── README.md              # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.11+
- Node.js 16+
- PostgreSQL (for production)
- Git

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/RajeshKc777/FURFEASTCO.git
cd FURFEASTCO/FURFEASTCO
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Node.js dependencies**
```bash
npm install
```

5. **Build TailwindCSS**
```bash
npm run build
```

6. **Set up environment variables**
Create `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=True
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
SUPABASE_BUCKET=your-bucket-name
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_SECRET=your-paypal-secret
```

7. **Run migrations**
```bash
python manage.py migrate
```

8. **Create superuser**
```bash
python manage.py createsuperuser
```

9. **Run development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

## ⚙️ Configuration

### Database Configuration
- **Development**: SQLite (default)
- **Production**: PostgreSQL

### Supabase Storage Setup
1. Create Supabase project
2. Create storage bucket
3. Set bucket to public
4. Add credentials to `.env`

### PayPal Integration
1. Create PayPal developer account
2. Get Client ID and Secret
3. Add to `.env`

## 📖 Usage

### Customer Workflow
1. **Browse Products**: Visit shop page or category pages
2. **Add to Cart**: Click "Add to Cart" on products
3. **Checkout**: Review cart and proceed to checkout
4. **Payment**: Pay via PayPal
5. **Track Order**: View order status in profile
6. **Chat Support**: Use chat icon for help

### Admin Workflow
1. **Login**: Access `/admin-login/`
2. **Dashboard**: View analytics at `/dashboard/`
3. **Manage Products**: Add/edit products
4. **Process Orders**: Update order status
5. **Customer Support**: Respond to chat messages
6. **Send Notifications**: Automatic on order updates

## 🔑 Key Features Explained

### 1. Real-time Notification System
- **Bell Icon**: Shows unread count
- **Types**: Order updates (📦) and messages (💬)
- **Visual Distinction**: Green border for orders, blue for messages
- **Auto-refresh**: Updates every 30 seconds
- **Clear All**: Delete all notifications

**Implementation**: `static/js/components.js`

### 2. Real-time Chat System
- **WebSocket**: Bidirectional communication
- **Typing Indicators**: Shows when user is typing
- **Online Status**: Green dot when online
- **Message History**: Persistent chat history
- **Admin Panel**: Centralized customer chat management

**Implementation**: `consumers.py`, `customer_chat.html`

### 3. Order Tracking
- **Status Updates**: Pending → Processing → Shipped → Delivered
- **Notifications**: Automatic on status change
- **Tracking Number**: Courier tracking integration
- **Timeline View**: Visual order progress

### 4. Profile Management
- **Profile Picture**: Upload via Supabase
- **Personal Info**: Name, email, phone, address
- **Order History**: View past orders
- **Wishlist**: Saved products

## 🗄️ Database Models

### Core Models
- **User**: Django auth user (extended with UserProfile)
- **UserProfile**: Profile picture, address, verification status
- **Product**: Name, price, category, stock, images
- **Order**: Order details, status, shipping info
- **OrderItem**: Products in order

### Marketing Models
- **FlashSale**: Time-limited discounts
- **PromoCode**: Discount codes
- **Blog**: Pet care articles
- **HeroImage**: Homepage sliders

### Communication Models
- **Notification**: User notifications (order/message)
- **CustomerMessage**: Chat messages
- **ContactMessage**: Contact form submissions

### Community Models
- **FurFeastFamily**: Pet owner community
- **Review**: Product reviews

## 🔌 API Endpoints

### Customer Endpoints
```
GET  /                          # Homepage
GET  /shop/                     # All products
GET  /dog-food/                 # Dog food category
GET  /cat-food/                 # Cat food category
GET  /accessories/              # Accessories category
GET  /product/<slug>/           # Product detail
POST /add-to-cart/              # Add to cart
GET  /cart/                     # View cart
POST /checkout/                 # Checkout
GET  /order-tracking/           # Track orders
GET  /customer-chat/            # Customer chat
GET  /api/notifications/        # Get notifications
POST /api/clear-all-notifications/ # Clear notifications
```

### Admin Endpoints
```
GET  /dashboard/                # Admin dashboard
GET  /dashboard/products/       # Product list
POST /dashboard/product/add/    # Add product
GET  /dashboard/orders/         # Order list
POST /dashboard/order/<id>/update/ # Update order
GET  /dashboard/customer-messages/ # Chat list
GET  /dashboard/customer-chat/<id>/ # Chat detail
GET  /dashboard/analytics/      # Business analytics
```

### WebSocket Endpoints
```
ws://localhost:8000/ws/chat/?customer_id=<id>  # Chat WebSocket
```

## 🎨 Customization

### Styling
- Edit `static/css/input.css` for custom styles
- Run `npm run build` to compile TailwindCSS

### Templates
- Customer templates: `templates/furfeast/`
- Admin templates: `templates/furfeast/dashboard/`

### Business Logic
- Customer views: `views.py`
- Admin views: `dashboard_views.py`

## 🐛 Troubleshooting

### Common Issues

**1. Static files not loading**
```bash
python manage.py collectstatic
```

**2. WebSocket connection failed**
- Check Daphne is running
- Verify ASGI configuration

**3. Images not uploading**
- Check Supabase credentials
- Verify bucket permissions

**4. Notifications not updating**
- Clear browser cache (Ctrl+Shift+R)
- Check CSRF token in cookies

## 📝 License

This project is private and proprietary.

## 👤 Author

**Rajesh KC**
- GitHub: [@RajeshKc777](https://github.com/RajeshKc777)

## 🙏 Acknowledgments

- Django Documentation
- TailwindCSS
- Supabase
- PayPal Developer

---

**Note**: This is a production-ready e-commerce platform. Ensure all environment variables are properly configured before deployment.
