# KoGidi (Backend Functionality)
🎓 KoGidi is an AI-powered offline learning platform designed for Nigerian students. It features a voice-activated homework assistant that understands English and native languages, recognizes Nigerian accents, and tracks student progress — making quality education accessible anywhere.

---

## Backend API Documentation

## Table of Contents

1. [Authentication Endpoints](#authentication-endpoints)
   1.1 [Login](#login)
   1.2 [Refresh Token](#refresh-token)
   1.3 [Logout](#logout)
2. [Student Endpoints](#student-endpoints)
   2.1 [List Students](#list-students)
   2.2 [Retrieve Student](#retrieve-student)
   2.3 [Create Student](#create-student)
   2.4 [Update Student](#update-student)
   2.5 [Delete Student](#delete-student)
3. [Teacher Endpoints](#teacher-endpoints)
4. [Parent Endpoints](#parent-endpoints)
5. [Security & Middleware](#security--middleware)
   5.1 [Cookie Settings](#cookie-settings)
   5.2 [JWT Settings](#jwt-settings)
   5.3 [Custom Middleware](#custom-middleware)
6. [Error Handling](#error-handling)
7. [Models & Data Schemas](#models--data-schemas)
8. [Changelog & Notes](#changelog--notes)

---

## Authentication Endpoints

All auth routes live under `/api/auth/`. Cookies are used to store tokens.
Requests must include `credentials: 'include'` on the client.

### Login

`POST /api/auth/login/`

Authenticate user and issue tokens in cookies.

**Request Body** (JSON)

```json
{
  "email": "user@example.com",
  "password": "P@ssw0rd!"
}
```

**Response** (200 OK)

* Sets two cookies:

  * `access_token` (HttpOnly, Secure, SameSite=Lax, max-age=900s)
  * `refresh_token` (HttpOnly, Secure, SameSite=Lax, max-age=604800s)

```json
{ "msg": "Login successful" }
```

**Errors**

* `400 Bad Request` – missing fields
* `401 Unauthorized` – invalid credentials

---

### Refresh Token

`POST /api/auth/refresh/`

Rotate access token using the refresh token cookie.

**Request**

* No body required. Browser sends `refresh_token` cookie automatically.

**Response** (200 OK)

* Sets new `access_token` cookie (HttpOnly, Secure, SameSite=Lax, max-age=900s)

```json
{ "msg": "Token refreshed" }
```

**Errors**

* `401 Unauthorized` – no refresh token
* `403 Forbidden` – invalid or expired refresh token

---

### Logout

`POST /api/auth/logout/`

Clear both auth cookies.

**Request**

* No body.

**Response** (200 OK)

* Deletes `access_token` and `refresh_token` cookies.

```json
{ "msg": "Logged out" }
```

---

## Student Endpoints

All student routes require a valid access token cookie. Permissions: only users with an active `StudentProfile`.

Base path: `/api/students/`

### List Students

`GET /api/students/`

**Response** (200 OK)

```json
[
  {
    "id": 1,
    "user": {
      "id": 10,
      "username": "jdoe",
      "email": "jdoe@example.com"
    },
    "date_of_birth": "2008-05-14",
    "enrollment_date": "2024-09-01",
    "grade_level": "Form 2",
    "is_active": true
  },
  ...
]
```

---

### Retrieve Student

`GET /api/students/{id}/`

**Response** (200 OK)

```json
{
  "id": 1,
  "user": { "id": 10, "username": "jdoe", "email": "jdoe@example.com" },
  "date_of_birth": "2008-05-14",
  "enrollment_date": "2024-09-01",
  "grade_level": "Form 2",
  "is_active": true
}
```

**Errors**

* `404 Not Found` – student does not exist
* `403 Forbidden` – no permission

---

### Create Student

`POST /api/students/`

**Request Body** (JSON)

```json
{
  "user_id": 15,
  "date_of_birth": "2009-02-21",
  "grade_level": "Grade 9"
}
```

**Response** (201 Created)

```json
{
  "id": 5,
  "user": { "id": 15, "username": "asmith", "email": "asmith@example.com" },
  "date_of_birth": "2009-02-21",
  "enrollment_date": "2025-05-24",
  "grade_level": "Grade 9",
  "is_active": true
}
```

**Errors**

* `400 Bad Request` – missing/invalid data
* `409 Conflict` – profile already exists

---

### Update Student

`PUT /api/students/{id}/`

**Request Body** (JSON)

```json
{
  "grade_level": "Grade 10",
  "is_active": false
}
```

**Response** (200 OK)

```json
{
  "id": 1,
  "grade_level": "Grade 10",
  "is_active": false,
  ...
}
```

---

### Delete Student

`DELETE /api/students/{id}/`

**Response**

* `204 No Content` on success.

---

## Teacher Endpoints

Mirror the student endpoints under `/api/teachers/`.
Use `TeacherProfile` model with fields like `department`, `hire_date`, `is_active`.

* `GET /api/teachers/`
* `GET /api/teachers/{id}/`
* `POST /api/teachers/`
* `PUT /api/teachers/{id}/`
* `DELETE /api/teachers/{id}/`

Permissions: only `TeacherProfile.is_active` users or admins.

---

## Parent Endpoints

Mirror similarly at `/api/parents/`.
Fields: `user`, `child_relations` (list of student IDs), `is_active`.

* `GET /api/parents/`
* `GET /api/parents/{id}/`
* `POST /api/parents/`
* `PUT /api/parents/{id}/`
* `DELETE /api/parents/{id}/`

---

## Security & Middleware

### Cookie Settings

* **HttpOnly:** prevents JS access → mitigates XSS
* **Secure:** send only over HTTPS
* **SameSite=Lax:** mitigates CSRF for most cross-site requests
* **max-age:**

  * `access_token`: 900 seconds (15 min)
  * `refresh_token`: 604800 seconds (7 days)

### JWT Settings (Django `settings.py`)

```python
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': (),  # we use cookies, not Authorization header
}
```

### Custom Middleware (`kogidi/middleware/jwt_middleware.py`)

```python
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.auth = JWTAuthentication()

    def __call__(self, request):
        token = request.COOKIES.get('access_token')
        if token:
            try:
                validated = self.auth.get_validated_token(token)
                request.user, _ = self.auth.get_user(validated), validated
            except AuthenticationFailed:
                request.user = None
        return self.get_response(request)
```

---

## Error Handling

All responses use standard HTTP status codes:

| Code | Meaning                                |
| ---- | -------------------------------------- |
| 200  | OK / Data returned                     |
| 201  | Created                                |
| 204  | No Content (successful delete)         |
| 400  | Bad Request (validation errors)        |
| 401  | Unauthorized (no/failing token)        |
| 403  | Forbidden (expired refresh, no access) |
| 404  | Not Found                              |
| 409  | Conflict (duplicate resource)          |
| 500  | Internal Server Error                  |

Error responses include JSON:

```json
{ "error": "Descriptive message" }
```

---

## Models & Data Schemas

### StudentProfile

```python
class StudentProfile(models.Model):
    user = OneToOneField(User, ...)
    date_of_birth = DateField(...)
    enrollment_date = DateField(...)
    grade_level = CharField(...)
    is_active = BooleanField(default=True)
```

### TeacherProfile & ParentProfile

Similar one-to-one extensions on `User` with their own fields:

* **TeacherProfile**: `department`, `hire_date`, `subjects`, `is_active`
* **ParentProfile**: `child_relations` (ManyToMany to Student), `is_active`

Use DRF serializers:

```python
class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"
```

---

## Changelog & Notes

* **2025-05-24**: Initial JWT cookie-based auth + student/teacher/parent scaffolding.
* **Next**: implement token blacklisting, admin roles, detailed audit logging, and rate-limiting.

---

<!-- *End of KoGidi API Documentation* -->
