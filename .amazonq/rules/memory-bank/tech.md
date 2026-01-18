# FurFeast Co. - Technology Stack

## Programming Languages

### Backend
- **Python 3.11+**: Primary backend language
- **Django 5.1.3**: Web framework

### Frontend
- **JavaScript (ES6+)**: Client-side interactivity
- **HTML5**: Template markup
- **CSS3**: Styling via TailwindCSS

### Configuration
- **YAML**: Docker Compose, Defang deployment
- **JSON**: Package management, configuration

## Core Dependencies

### Backend Framework & Extensions
```
Django==5.1.3                    # Web framework
channels==4.0.0                  # WebSocket support
daphne==4.0.0                    # ASGI server
psycopg2-binary==2.9.7          # PostgreSQL adapter
whitenoise==6.5.0               # Static file serving
```

### Storage & External Services
```
supabase==2.8.0                 # Cloud storage client
Pillow==10.0.0                  # Image processing
requests==2.31.0                # HTTP client
websockets==12.0                # WebSocket protocol
```

### Configuration Management
```
python-decouple==3.8            # Environment variables
python-dotenv==1.0.0            # .env file support
```

### Frontend Build Tools
```json
{
  "devDependencies": {
    "tailwindcss": "^3.4.19",   // Utility-first CSS
    "postcss": "^8.5.6",        // CSS processing
    "autoprefixer": "^10.4.23"  // CSS vendor prefixes
  }
}
```

## Database Systems

### Development
- **SQLite**: File-based database (db.sqlite3)
- Zero configuration, included with Python

### Production
- **PostgreSQL**: Relational database
- Configured via DATABASE_URL environment variable

## Real-time Infrastructure

### WebSocket Stack
- **Django Channels**: WebSocket integration for Django
- **Daphne**: ASGI server for WebSocket connections
- **Redis** (implied): Channel layer backend for message routing

### Communication Protocol
- **WebSocket**: Bidirectional real-time communication
- **ASGI**: Asynchronous Server Gateway Interface

## Storage Solutions

### Local Development
- **File System**: Django default storage
- Media files in `media/` directory

### Production
- **Supabase Storage**: Cloud-based object storage
- Custom storage backend in `storage.py`
- Public bucket for product images and profiles

## Payment Integration
- **PayPal SDK**: Payment gateway
- Client ID and Secret via environment variables

## Frontend Technologies

### CSS Framework
- **TailwindCSS 3.4.19**: Utility-first CSS framework
- JIT (Just-In-Time) compilation
- Custom configuration in `tailwind.config.js`

### JavaScript Architecture
- **Vanilla JS**: No framework dependencies
- **WebSocket API**: Native browser WebSocket
- **Fetch API**: AJAX requests
- **ES6 Modules**: Component-based organization

## Development Tools

### Build System
```bash
# TailwindCSS compilation
npm run build                    # Build CSS for production
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

### Django Management
```bash
# Database operations
python manage.py makemigrations  # Create migration files
python manage.py migrate         # Apply migrations
python manage.py createsuperuser # Create admin user

# Development server
python manage.py runserver       # HTTP server (dev)
daphne -b 0.0.0.0 -p 8000 FURFEASTCO.asgi:application  # ASGI server

# Static files
python manage.py collectstatic   # Gather static files

# Custom commands
python manage.py <custom_command>  # Run management commands
```

### Testing & Verification
```bash
python verify_migration.py before  # Pre-migration check
python verify_migration.py after   # Post-migration verification
python health_check.py             # Application health check
```

## Containerization

### Docker
```dockerfile
# Base: Python 3.11
# Server: Daphne (ASGI)
# Static: WhiteNoise
```

### Docker Compose
```yaml
# Services: web, db (PostgreSQL)
# Volumes: media files, static files
# Networks: Internal bridge network
```

## Deployment Platform

### Defang
- **Configuration**: defang.yaml
- **Commands**:
  ```bash
  deploy.bat              # Windows deployment script
  deploy_check.bat        # Pre-deployment validation
  ```

## Environment Configuration

### Required Environment Variables
```env
# Django
SECRET_KEY=<django-secret-key>
DEBUG=True|False
ALLOWED_HOSTS=<comma-separated-hosts>

# Database (Production)
DATABASE_URL=postgresql://user:pass@host:port/db

# Supabase Storage
SUPABASE_URL=<supabase-project-url>
SUPABASE_KEY=<supabase-anon-key>
SUPABASE_BUCKET=<bucket-name>

# PayPal
PAYPAL_CLIENT_ID=<paypal-client-id>
PAYPAL_SECRET=<paypal-secret>
PAYPAL_MODE=sandbox|live

# Email (Optional)
EMAIL_HOST=<smtp-host>
EMAIL_PORT=<smtp-port>
EMAIL_HOST_USER=<email>
EMAIL_HOST_PASSWORD=<password>
```

## Development Workflow

### Initial Setup
```bash
# 1. Clone repository
git clone <repository-url>
cd FURFEASTCO/FURFEASTCO

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/Mac

# 3. Install dependencies
pip install -r requirements.txt
npm install

# 4. Build frontend
npm run build

# 5. Configure environment
# Create .env file with required variables

# 6. Initialize database
python manage.py migrate
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

### Development Commands
```bash
# Start development with auto-reload
python manage.py runserver

# Watch TailwindCSS changes
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch

# Create new app
python manage.py startapp <app_name>

# Django shell
python manage.py shell

# Database shell
python manage.py dbshell
```

## Version Control
- **Git**: Source control
- **.gitignore**: Excludes venv, db.sqlite3, .env, media files
- **.dockerignore**: Excludes development files from Docker builds

## Code Quality Tools
- **Django Debug Toolbar** (implied for development)
- **Python Type Hints**: Modern Python typing
- **ESLint/Prettier** (recommended for JavaScript)

## Browser Compatibility
- Modern browsers with WebSocket support
- ES6+ JavaScript features
- CSS Grid and Flexbox
