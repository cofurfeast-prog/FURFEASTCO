# FurFeast Co. - Project Structure

## Directory Organization

```
FURFEASTCO/
├── FURFEASTCO/                    # Django project root
│   ├── furfeast/                  # Main application package
│   │   ├── management/            # Custom Django management commands
│   │   ├── migrations/            # Database migration files
│   │   ├── static/                # Static assets (CSS, JS, images)
│   │   │   ├── css/               # Compiled TailwindCSS
│   │   │   └── js/                # JavaScript modules
│   │   │       ├── components.js  # Notification system
│   │   │       ├── main.js        # Core application logic
│   │   │       └── slider.js      # Image carousel functionality
│   │   ├── templates/             # Django HTML templates
│   │   │   └── furfeast/
│   │   │       ├── dashboard/     # Admin panel templates
│   │   │       └── *.html         # Customer-facing templates
│   │   ├── templatetags/          # Custom template filters/tags
│   │   ├── tests/                 # Test suite
│   │   ├── admin.py               # Django admin configuration
│   │   ├── api_views.py           # REST API endpoints
│   │   ├── apps.py                # App configuration
│   │   ├── consumers.py           # WebSocket consumers (Channels)
│   │   ├── context_processors.py  # Global template context
│   │   ├── dashboard_views.py     # Admin dashboard views
│   │   ├── models.py              # Database models
│   │   ├── routing.py             # WebSocket URL routing
│   │   ├── signals.py             # Django signal handlers
│   │   ├── storage.py             # Supabase storage backend
│   │   ├── urls.py                # URL routing configuration
│   │   └── views.py               # Customer-facing views
│   │
│   ├── FURFEASTCO/                # Project settings package
│   │   ├── asgi.py                # ASGI configuration (WebSocket)
│   │   ├── production.py          # Production-specific settings
│   │   ├── settings.py            # Main Django settings
│   │   ├── urls.py                # Root URL configuration
│   │   └── wsgi.py                # WSGI configuration
│   │
│   ├── media/                     # User-uploaded files
│   │   └── profiles/              # Profile pictures
│   │
│   ├── .env                       # Environment variables (local)
│   ├── .env.deploy                # Deployment environment config
│   ├── compose.yaml               # Docker Compose configuration
│   ├── db.sqlite3                 # SQLite database (development)
│   ├── defang.yaml                # Defang deployment config
│   ├── Dockerfile                 # Docker image definition
│   ├── manage.py                  # Django management script
│   ├── package.json               # Node.js dependencies (TailwindCSS)
│   ├── requirements.txt           # Python dependencies
│   ├── tailwind.config.js         # TailwindCSS configuration
│   └── *.md                       # Documentation files
│
└── README.md                      # Project documentation
```

## Core Components

### Application Layer (furfeast/)

**Views Architecture**
- `views.py`: Customer-facing views (shop, cart, checkout, profile)
- `dashboard_views.py`: Admin panel views (analytics, orders, products)
- `api_views.py`: JSON API endpoints for AJAX operations

**Real-time Communication**
- `consumers.py`: WebSocket consumers for chat functionality
- `routing.py`: WebSocket URL routing configuration
- Uses Django Channels for bidirectional communication

**Data Layer**
- `models.py`: Database schema definitions
  - User management (UserProfile, EmailVerification)
  - Product catalog (Product, Category)
  - Order processing (Order, OrderItem)
  - Communication (CustomerMessage, ChatRoom, Notification)
  - Marketing (FlashSale, PromoCode, Blog)
  - Community (FurFeastFamily, Review)

**Storage Integration**
- `storage.py`: Custom Supabase storage backend
- Handles file uploads (product images, profile pictures)
- Cloud-based storage for scalability

**Signal Handlers**
- `signals.py`: Automated actions on model events
- Order status change notifications
- User registration workflows

### Configuration Layer (FURFEASTCO/)

**Settings Management**
- `settings.py`: Base configuration (database, apps, middleware)
- `production.py`: Production overrides (PostgreSQL, security)
- Environment-based configuration via python-decouple

**Server Configuration**
- `asgi.py`: ASGI application for WebSocket support (Daphne)
- `wsgi.py`: WSGI application for HTTP requests (Gunicorn)
- Dual-protocol support for real-time features

### Frontend Layer

**Static Assets**
- `static/css/`: TailwindCSS compiled output
- `static/js/components.js`: Notification bell system
- `static/js/main.js`: Cart, wishlist, form handling
- `static/js/slider.js`: Hero image carousel

**Templates**
- Customer templates: Product pages, cart, checkout, profile
- Dashboard templates: Analytics, order management, chat interface
- Base template with shared navigation and notifications

## Architectural Patterns

### MVC Pattern (Django MVT)
- **Models**: Database schema in `models.py`
- **Views**: Business logic in `views.py`, `dashboard_views.py`
- **Templates**: HTML presentation layer

### Real-time Architecture
- **WebSocket Layer**: Django Channels with Redis channel layer
- **Consumer Pattern**: AsyncWebsocketConsumer for chat
- **Group Broadcasting**: Room-based message distribution

### Storage Pattern
- **Custom Backend**: Supabase storage integration
- **Abstraction**: Django storage API compliance
- **Cloud-first**: Scalable file management

### API Design
- **REST Endpoints**: JSON responses for AJAX operations
- **Authentication**: Login-required decorators
- **CSRF Protection**: Token-based security

### Notification System
- **Push Model**: Server-initiated notifications
- **Polling Fallback**: 30-second refresh for reliability
- **Type Distinction**: Order updates vs. chat messages

## Component Relationships

```
Customer Request → URLs → Views → Models → Database
                    ↓
                Templates → Static Assets → Browser

WebSocket Request → Routing → Consumers → Channel Layer → Broadcast
                                ↓
                            Database (Messages)

File Upload → Storage Backend → Supabase → Cloud Storage
```

## Database Schema Relationships

- User ←→ UserProfile (one-to-one)
- User ←→ ChatRoom (one-to-one)
- ChatRoom ←→ CustomerMessage (one-to-many)
- User ←→ Order (one-to-many)
- Order ←→ OrderItem (one-to-many)
- Product ←→ OrderItem (one-to-many)
- User ←→ Notification (one-to-many)
- Product ←→ Review (one-to-many)

## Deployment Architecture

**Development**
- SQLite database
- Django development server
- Local file storage

**Production**
- PostgreSQL database
- Daphne ASGI server (WebSocket)
- Gunicorn WSGI server (HTTP)
- Supabase cloud storage
- Docker containerization
- Defang platform deployment
