# KoGidi Learning Platform - Backend

Django REST API for the KoGidi learning management system.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- pip & virtualenv

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Configure .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## 📁 Project Structure

```
KoGidi-BE/
├── kogidi/              # Main project settings
│   ├── settings.py     # Django configuration
│   ├── urls.py         # URL routing
│   └── wsgi.py         # WSGI config
├── accounts/           # User authentication
├── students/           # Student profiles
├── teachers/           # Teacher profiles
├── parents/            # Parent profiles
├── courses/            # Courses & content
│   ├── models.py      # Database models
│   ├── views.py       # API endpoints
│   ├── serializers.py # Data serialization
│   └── management/    # Management commands
└── manage.py          # Django CLI
```

## 🎯 Key Features

- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **Role-Based Access** - Student, Teacher, Parent roles
- ✅ **API Rate Limiting** - Prevents abuse
- ✅ **Database Optimization** - 12 performance indexes
- ✅ **CORS Configured** - Secure cross-origin requests
- ✅ **API Documentation** - Swagger/OpenAPI
- ✅ **Data Validation** - Strong validation rules

## 🛠️ Tech Stack

- **Framework:** Django 5.2 + Django REST Framework
- **Database:** MySQL 8.0
- **Authentication:** JWT (djangorestframework-simplejwt)
- **API Docs:** drf-yasg (Swagger)
- **CORS:** django-cors-headers
- **Environment:** python-dotenv

## 📦 Key Packages

```
Django==5.2.1
djangorestframework==3.15.2
djangorestframework-simplejwt==5.4.0
mysqlclient==2.2.6
django-cors-headers==4.6.0
drf-yasg==1.21.8
python-dotenv==1.0.1
```

## 🔧 Configuration

### Environment Variables

Create `.env` file (see `.env.example`):

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DB_NAME=kogidi_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# JWT
JWT_ACCESS_TOKEN_EXPIRES_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRES_DAYS=7
```

### Database Setup

```bash
# Create database
mysql -u root -p
CREATE DATABASE kogidi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Run migrations
python manage.py migrate

# Seed sample data
python manage.py seed_all_data
```

## 🗄️ Database Models

### Core Models
- **User** - Custom user model (accounts)
- **Student** - Student profiles
- **Teacher** - Teacher profiles
- **Parent** - Parent profiles
- **Course** - Learning courses
- **StudentProgress** - Course progress tracking
- **Assignment** - Assignments & submissions
- **Achievement** - Student achievements
- **StudentStats** - Statistics aggregation

### Relationships
- User → Student/Teacher/Parent (One-to-One)
- Student → Courses (Many-to-Many via Progress)
- Parent → Students (Many-to-Many via Relationship)
- Course → Assignments (One-to-Many)

## 🚀 API Endpoints

### Authentication
```
POST /api/v1/accounts/register/     # Register new user
POST /api/v1/accounts/login/        # Login
POST /api/v1/accounts/refresh/      # Refresh JWT token
POST /api/v1/accounts/logout/       # Logout
```

### Students
```
GET  /api/v1/students/profile/      # Get student profile
PUT  /api/v1/students/profile/update/ # Update profile
```

### Teachers
```
GET  /api/v1/teachers/profile/      # Get teacher profile
GET  /api/v1/teachers/dashboard/    # Teacher dashboard data
PUT  /api/v1/teachers/profile/update/ # Update profile
```

### Parents
```
GET  /api/v1/parents/profile/       # Get parent profile
GET  /api/v1/parents/dashboard/     # Parent dashboard data
```

### Courses
```
GET  /api/v1/courses/               # List courses
GET  /api/v1/courses/{id}/          # Course details
GET  /api/v1/courses/my_courses/    # User's enrolled courses
```

### Dashboard
```
GET  /api/v1/dashboard/             # Student dashboard data
```

### Progress
```
GET  /api/v1/progress/              # Student progress
POST /api/v1/progress/              # Update progress
```

### Assignments
```
GET  /api/v1/assignments/           # List assignments
POST /api/v1/assignments/{id}/submit/ # Submit assignment
```

### Achievements
```
GET  /api/v1/achievements/          # List achievements
```

## 🔐 Security Features

### Authentication & Authorization
- JWT tokens with HttpOnly cookies
- Token refresh mechanism
- Role-based permissions
- Rate limiting (5 login attempts/min)

### Data Protection
- Password validators (8+ chars, complexity)
- HTTPS enforcement (production)
- HSTS headers
- Secure cookie configuration
- Input validation

### Attack Prevention
- Rate limiting (100/hour anon, 1000/hour auth)
- CORS properly configured
- CSRF protection
- XSS prevention headers
- SQL injection protection (Django ORM)

## 📊 Performance Optimizations

### Database
- 12 strategic indexes on frequently queried fields
- `select_related()` for foreign keys
- `prefetch_related()` for reverse relations
- Query optimization in viewsets

### API
- Pagination (default: 10 items/page)
- Response caching (planned)
- Efficient serializers
- Optimized querysets

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test courses

# Run with coverage
coverage run manage.py test
coverage report
```

## 📝 Management Commands

```bash
# Seed database with sample data
python manage.py seed_all_data

# Create admin user
python manage.py createsuperuser

# Clear database (careful!)
python reset_db.py
```

## 🚀 Deployment

### Production Checklist

```bash
# 1. Update .env
DEBUG=False
SECRET_KEY=<generate-strong-key>

# 2. Collect static files
python manage.py collectstatic

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Check deployment
python manage.py check --deploy
```

### Deploy to Render/Railway/Heroku

```bash
# Install gunicorn
pip install gunicorn

# Add to requirements.txt

# Create Procfile
web: gunicorn kogidi.wsgi

# Deploy
git push heroku main
```

## 📚 API Documentation

Access Swagger UI at:
- Development: `http://localhost:8000/api/docs/`
- Redoc: `http://localhost:8000/api/redoc/`

## 🔧 Development

### Code Style
- Follow PEP 8
- Use Django best practices
- Type hints encouraged
- Docstrings for all functions

### Git Workflow
1. Create feature branch
2. Make changes
3. Add tests
4. Submit PR

## 🐛 Common Issues

### Database Connection Error
```bash
# Check MySQL is running
service mysql status

# Check credentials in .env
# Verify database exists
```

### Migration Issues
```bash
# Reset migrations (development only)
python manage.py migrate --fake-initial

# Or delete and recreate DB
```

## 📄 License

Proprietary - KoGidi Platform

---

**Built with 🐍 by the KoGidi Team**
