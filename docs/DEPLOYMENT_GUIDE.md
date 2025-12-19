# 🚀 KoGidi Platform - Deployment Guide

Complete guide for deploying KoGidi to production.

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Database Migration](#database-migration)
6. [SSL/HTTPS Setup](#sslhttps-setup)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)

---

## 🔍 Pre-Deployment Checklist

### Backend:
- [ ] Set `DEBUG=False` in production .env
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up static/media file storage
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS enforcement
- [ ] Set up email service (if needed)
- [ ] Configure CORS allowed origins
- [ ] Run security check: `python manage.py check --deploy`

### Frontend:
- [ ] Set production API URL in .env
- [ ] Build optimized bundle
- [ ] Configure CDN (optional)
- [ ] Set up error tracking (Sentry)
- [ ] Configure analytics
- [ ] Test in production mode locally

### Infrastructure:
- [ ] Purchase domain name
- [ ] Set up DNS records
- [ ] Obtain SSL certificate
- [ ] Configure firewall rules
- [ ] Set up backup system
- [ ] Configure monitoring alerts

---

## 🔧 Environment Setup

### 1. Backend Environment Variables

Create `KoGidi-BE/.env`:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-very-strong-secret-key-here-change-this
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=kogidi_production
DB_USER=kogidi_user
DB_PASSWORD=strong_password_here
DB_HOST=your-db-host.com
DB_PORT=3306

# JWT
JWT_ACCESS_TOKEN_EXPIRES_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRES_DAYS=7

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 2. Frontend Environment Variables

Create `KoGidi-FE/.env.production`:

```bash
VITE_API_URL=https://api.yourdomain.com
VITE_APP_NAME=KoGidi
VITE_APP_VERSION=1.0.0
```

---

## 🐳 Docker Deployment

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/your-org/kogidi.git
cd kogidi

# 2. Create .env file
cp .env.example .env
# Edit .env with production values

# 3. Build and start
docker-compose up -d --build

# 4. Run migrations
docker-compose exec backend python manage.py migrate

# 5. Create superuser
docker-compose exec backend python manage.py createsuperuser

# 6. Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

### Verify Deployment

```bash
# Check services
docker-compose ps

# View logs
docker-compose logs -f

# Check backend health
curl http://localhost:8000/api/v1/

# Check frontend
curl http://localhost/
```

---

## ☁️ Cloud Deployment

### Option 1: Render.com

#### Backend:
1. Create new Web Service
2. Connect GitHub repository
3. Configure:
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn kogidi.wsgi:application`
4. Add environment variables
5. Deploy

#### Frontend:
1. Create new Static Site
2. Connect GitHub repository
3. Configure:
   - Build Command: `npm run build`
   - Publish Directory: `dist`
4. Add environment variables
5. Deploy

### Option 2: Vercel (Frontend) + Railway (Backend)

#### Frontend on Vercel:
```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend
cd KoGidi-FE

# Deploy
vercel --prod

# Set environment variables in dashboard
```

#### Backend on Railway:
1. Create new project
2. Add MySQL database
3. Add Django service
4. Connect GitHub
5. Configure environment variables
6. Deploy

### Option 3: AWS

#### EC2 Setup:
```bash
# 1. Launch EC2 instance (Ubuntu 22.04)

# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Install Docker Compose
sudo apt-get install docker-compose

# 5. Clone repository
git clone https://github.com/your-org/kogidi.git
cd kogidi

# 6. Deploy
docker-compose up -d
```

#### RDS for Database:
1. Create MySQL RDS instance
2. Configure security groups
3. Update backend .env with RDS endpoint
4. Run migrations

#### S3 for Static Files:
```python
# settings.py
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'kogidi-static'
AWS_S3_REGION_NAME = 'us-east-1'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## 🗄️ Database Migration

### Initial Setup:
```bash
# Create database
mysql -u root -p
CREATE DATABASE kogidi_production CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'kogidi_user'@'%' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON kogidi_production.* TO 'kogidi_user'@'%';
FLUSH PRIVILEGES;

# Run migrations
python manage.py migrate

# Load initial data (optional)
python manage.py seed_all_data
```

### Backup & Restore:
```bash
# Backup
mysqldump -u kogidi_user -p kogidi_production > backup_$(date +%Y%m%d).sql

# Restore
mysql -u kogidi_user -p kogidi_production < backup_20250119.sql
```

---

## 🔒 SSL/HTTPS Setup

### Option 1: Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Option 2: Cloudflare (Free + CDN)

1. Add site to Cloudflare
2. Update nameservers
3. Enable "Full (strict)" SSL
4. Enable "Always Use HTTPS"
5. Configure page rules

---

## 📊 Monitoring

### Application Monitoring (Sentry)

```bash
# Install Sentry SDK
pip install sentry-sdk

# Configure in settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### Server Monitoring

```bash
# Install monitoring tools
sudo apt-get install htop nethogs

# Check resource usage
htop

# Monitor network
sudo nethogs

# Check logs
journalctl -u your-service -f
```

### Database Monitoring

```bash
# MySQL slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

# Check connections
SHOW FULL PROCESSLIST;

# Check database size
SELECT table_schema "Database", 
  ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) "Size (MB)" 
FROM information_schema.TABLES 
GROUP BY table_schema;
```

---

## 🐛 Troubleshooting

### Backend Issues

**500 Internal Server Error:**
```bash
# Check logs
docker-compose logs backend

# Debug mode (temporarily)
DEBUG=True python manage.py runserver

# Check database connection
python manage.py dbshell
```

**Static Files Not Loading:**
```bash
# Collect static files
python manage.py collectstatic --clear --noinput

# Check STATIC_ROOT setting
python manage.py findstatic admin/css/base.css
```

**Database Connection Error:**
```bash
# Test database connection
python manage.py check --database default

# Verify credentials in .env
# Check database server status
```

### Frontend Issues

**Blank Page After Deploy:**
```bash
# Check console for errors
# Verify API_URL is correct
# Check CORS settings on backend
# Rebuild with correct environment variables
```

**API Calls Failing:**
```bash
# Check network tab in DevTools
# Verify API endpoint URLs
# Check CORS headers
# Verify authentication tokens
```

---

## 🔄 CI/CD Setup (Optional)

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd kogidi
          git pull
          docker-compose down
          docker-compose up -d --build
          docker-compose exec backend python manage.py migrate
          docker-compose exec backend python manage.py collectstatic --noinput
```

---

## 📝 Post-Deployment

### Verify Everything Works:
- [ ] Homepage loads
- [ ] User can register/login
- [ ] API endpoints respond
- [ ] Database operations work
- [ ] Static files load
- [ ] HTTPS is enforced
- [ ] Email works (if configured)
- [ ] Admin panel accessible

### Performance Testing:
```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 https://yourdomain.com/

# Check page speed
# Use Google PageSpeed Insights
# Use GTmetrix
```

---

## 🆘 Support

If you encounter issues:
1. Check logs first
2. Review environment variables
3. Verify database connection
4. Check firewall rules
5. Consult documentation
6. Contact support

---

**🎉 Congratulations! Your KoGidi platform is now live!**

*Last Updated: 2025-12-19*
