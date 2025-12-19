# 🚀 KoGidi - Quick Start Guide (Post Bug Fixes)

This guide will help you get KoGidi up and running after the bug fixes.

---

## 📋 Prerequisites

- **Python 3.10+** installed
- **Node.js 18+** and npm installed
- **MySQL 8.0+** installed and running
- Git installed

---

## 🔧 Backend Setup

### 1. Navigate to Backend Directory
```bash
cd KoGidi-BE
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and update:
```env
DB_NAME=kogidi_db
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=generate-a-random-secret-key-here
```

### 5. Create Database
```bash
mysql -u root -p
```
```sql
CREATE DATABASE kogidi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Start Development Server
```bash
python manage.py runserver
```

Backend should now be running at: **http://localhost:8000**

---

## 💻 Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd KoGidi-FE
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment (Optional)
```bash
cp .env.example .env.local
```

Edit `.env.local` if you need to change API URL:
```env
VITE_API_URL=http://localhost:8000
```

### 4. Start Development Server
```bash
npm run dev
```

Frontend should now be running at: **http://localhost:8080**

---

## ✅ Verify Setup

### 1. Check Backend
- Visit http://localhost:8000/admin
- Visit http://localhost:8000/swagger for API docs

### 2. Check Frontend
- Visit http://localhost:8080
- You should see the KoGidi landing page

### 3. Test Authentication
1. Click "Sign Up" on the landing page
2. Fill out the registration form
3. Check browser DevTools > Application > Cookies
   - You should see `access_token` and `refresh_token`
4. Check DevTools > Console
   - You should see API Client logs
5. You should be redirected to dashboard

---

## 🐛 Common Issues & Solutions

### Issue: "django.core.exceptions.ImproperlyConfigured: mysqlclient"
**Solution:** Install MySQL client
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

# macOS
brew install mysql-client
```

### Issue: "CORS policy" error in browser
**Solution:** Verify backend is running on port 8000 and frontend on 8080

### Issue: "Access token not found"
**Solution:** 
1. Clear browser cookies
2. Make sure backend is running
3. Check browser console for API errors

### Issue: Frontend shows 404 for API calls
**Solution:** Verify `.env` or check `src/services/apiClient.ts` has correct URL

---

## 🔐 Security Notes

**IMPORTANT BEFORE DEPLOYMENT:**

1. Change `SECRET_KEY` in `.env`
2. Set `DEBUG=False` in production
3. Update `ALLOWED_HOSTS` with your domain
4. Set `CORS_ALLOW_ALL_ORIGINS=False`
5. Use HTTPS in production
6. Change default database password

---

## 📚 Next Steps

1. Read `BUG_FIXES.md` for details on what was fixed
2. Explore the Swagger documentation at /swagger
3. Review user roles (Student, Teacher, Parent)
4. Test offline features
5. Explore voice assistant functionality

---

## 🆘 Getting Help

If you encounter issues:

1. Check `BUG_FIXES.md` for known issues
2. Verify all prerequisites are installed
3. Check browser console for errors
4. Check backend terminal for errors
5. Verify database is running and accessible

---

## 📝 Development Workflow

### Backend Changes
```bash
# After model changes
python manage.py makemigrations
python manage.py migrate

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

### Frontend Changes
```bash
# Linting
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

---

**Happy Coding! 🎉**
