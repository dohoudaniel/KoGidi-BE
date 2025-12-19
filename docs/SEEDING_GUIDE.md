# 🌱 Database Seeding Guide (Updated)

## Overview
This command seeds the KoGidi database with test data for **existing users**. It does NOT create new users.

## ⚠️ Important: Create Users First!

Before running the seed command, you need to have users in your database. You can:

1. **Create users via Django Admin:**
   ```
   http://localhost:8000/admin/
   ```

2. **Create users via Signup:**
   ```
   http://localhost:8080/signup
   ```

3. **Create a superuser:**
   ```bash
   python3 manage.py createsuperuser
   ```

## What Gets Created

The seeding command will create data for **all existing users** in your database:

### For Students:
- ✅ Course enrollments (2-4 courses per student)
- ✅ Progress tracking (10-95% completion)
- ✅ Student stats (courses, hours, streak, scores)
- ✅ Achievements (1-3 per student)
- ✅ Assignments (assigned to each student)

### For Teachers:
- ✅ Teacher classes (2-3 per teacher)
- ✅ Teacher stats (students, courses, pending grading)
- ✅ Class progress metrics

### For Parents:
- ✅ Links to students (1-2 students per parent)

### For All:
- ✅ 8 Courses (if they don't exist)
- ✅ Assignments (2-4 per course, distributed to students)

## How to Run

### Step 1: Ensure You Have Users
```bash
# Check if you have users
python3 manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> print(f"Students: {User.objects.filter(student_profile__isnull=False).count()}")
>>> print(f"Teachers: {User.objects.filter(teacher_profile__isnull=False).count()}")
>>> print(f"Parents: {User.objects.filter(parent_profile__isnull=False).count()}")
>>> exit()
```

### Step 2: Run Seed Command
```bash
cd KoGidi-BE
python3 manage.py seed_all_data
```

### Expected Output:
```
🌱 Starting database seeding (using existing users)...

📚 Ensuring courses exist...
  ✅ Created course: Introduction to Mathematics
  (or)
  ℹ️  Course exists: Introduction to Mathematics
  
📈 Creating student progress data...
  ✅ Progress: student@email.com → Mathematics
  ✅ Progress: student@email.com → Science
  
👨‍🏫 Creating teacher data...
  ✅ Class: Introduction to Mathematics - PRIMARY 4
  
👨‍👩‍👧 Linking parents to students...
  ✅ Linked: parent@email.com → student@email.com
  
📝 Creating assignments...
  ✅ Created 45 assignments

✅ Database seeding completed successfully!
📊 Summary:
   - Students: 3
   - Teachers: 1
   - Parents: 1
   - Courses: 8
   - Data created for all existing users
```

## What If I Have No Users?

If you run the command with no users, you'll see:
```
⚠️  No students found. Please create student users first.
```

**Solution:** Create users first via:
1. Signup page (http://localhost:8080/signup)
2. Django admin (http://localhost:8000/admin/)

## Testing After Seeding

### With Your Own User:
1. **Signup** at http://localhost:8080/signup
2. **Run seed:** `python3 manage.py seed_all_data`
3. **Login** with your account
4. **Check dashboard** - should now have:
   - Courses enrolled (2-4)
   - Progress percentages
   - Achievements
   - Assignments

## Sample Data Characteristics

### Students (Using Your Users):
- **Enrollments:** 2-4 courses per student
- **Progress:** 10-95% per course
- **Time Spent:** 60-500 minutes per course
- **Scores:** 60-95%
- **Streaks:** 1-14 days
- **Achievements:** 1-3 per student

### Teachers (Using Your Users):
- **Classes:** 2-3 per teacher
- **Students per Class:** 10-25
- **Class Progress:** 30-85%
- **Pending Grading:** 5-20 assignments

### Assignments:
- **Types:** Quiz, Essay, Project, Homework, Presentation
- **Priorities:** High, Medium, Low
- **Statuses:** Pending, Submitted, Graded
- **Due Dates:** 1-30 days from now
- **Distribution:** 3-7 students per assignment

## Courses Created

The command ensures these 8 courses exist:
1. Introduction to Mathematics (Primary 4)
2. Basic Science (Primary 5)
3. Yoruba Language (Primary 3)
4. English Language (JSS 1)
5. Computer Studies (JSS 2)
6. Social Studies (Primary 6)
7. Basic Technology (JSS 1)
8. Agricultural Science (JSS 3)

## Can I Run It Multiple Times?

**Yes!** The command uses `get_or_create()` and `update_or_create()`, so:
- ✅ Safe to run multiple times
- ✅ Won't create duplicate data
- ✅ Will update existing stats
- ✅ Will create new data for new users

## Troubleshooting

### Error: "No students found"
**Solution:** Create at least one student user via signup or admin panel.

### Error: "table does not exist"
**Solution:** Run migrations first:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Want Fresh Data?
```bash
# Delete existing data (keeps users)
python3 manage.py shell
>>> from courses.models import *
>>> StudentProgress.objects.all().delete()
>>> Assignment.objects.all().delete()
>>> Achievement.objects.all().delete()
>>> StudentStats.objects.all().delete()
>>> TeacherClass.objects.all().delete()
>>> TeacherStats.objects.all().delete()
>>> exit()

# Run seeding again
python3 manage.py seed_all_data
```

## Recommended Workflow

### For Development:
```bash
# 1. Create test users via signup
# Visit: http://localhost:8080/signup
# Create 2-3 students, 1 teacher, 1 parent

# 2. Run migrations (if needed)
python3 manage.py makemigrations teachers
python3 manage.py migrate

# 3. Seed data
python3 manage.py seed_all_data

# 4. Test the application
# Login with any user you created
```

### For Testing:
```bash
# Seed, test, reseed as needed
python3 manage.py seed_all_data
# Test feature
# Delete specific data if needed
# Run again
python3 manage.py seed_all_data
```

## What Changes From Previous Version?

**Old Command** (❌ Don't use):
- Created 20 new users
- Had hardcoded emails/passwords
- Caused user_type field error

**New Command** (✅ Use this):
- Works with YOUR existing users
- No user creation
- No password management
- Works with any user count

## Next Steps

1. ✅ Create users (via signup or admin)
2. ✅ Run: `python3 manage.py seed_all_data`
3. ✅ Test all dashboards
4. ✅ Verify data is showing

---

**Happy Testing! 🎉**

Remember: This command works with YOUR users, not predefined test users!
