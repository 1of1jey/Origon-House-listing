# Authentication API Documentation

This Django REST Framework authentication system provides the following API endpoints:

## Base URL

All authentication endpoints are prefixed with `/auth/api/`

## Endpoints

### 1. User Registration

**POST** `/auth/api/register/`

Register a new user with full name, phone number, and email.

**Request Body:**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```

**Response (201 Created):**

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "date_joined": "2023-10-10T10:30:00Z",
    "is_active": true
  },
  "token": "your_auth_token_here"
}
```

### 2. User Login

**POST** `/auth/api/login/`

Login with email and password.

**Request Body:**

```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**

```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "date_joined": "2023-10-10T10:30:00Z",
    "is_active": true
  },
  "token": "your_auth_token_here"
}
```

### 3. User Logout

**POST** `/auth/api/logout/`

Logout the current user (requires authentication).

**Headers:**

```
Authorization: Token your_auth_token_here
```

**Response (200 OK):**

```json
{
  "message": "Successfully logged out"
}
```

### 4. Get User Profile

**GET** `/auth/api/profile/`

Get the current user's profile information (requires authentication).

**Headers:**

```
Authorization: Token your_auth_token_here
```

**Response (200 OK):**

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "date_joined": "2023-10-10T10:30:00Z",
  "is_active": true
}
```

### 5. Update User Profile

**PATCH** `/auth/api/profile/`

Update the current user's profile information (requires authentication).

**Headers:**

```
Authorization: Token your_auth_token_here
```

**Request Body:**

```json
{
  "full_name": "John Smith",
  "phone_number": "+0987654321"
}
```

**Response (200 OK):**

```json
{
  "full_name": "John Smith",
  "phone_number": "+0987654321"
}
```

### 6. Change Password

**POST** `/auth/api/change-password/`

Change the current user's password (requires authentication).

**Headers:**

```
Authorization: Token your_auth_token_here
```

**Request Body:**

```json
{
  "old_password": "currentpassword123",
  "new_password": "newpassword456",
  "new_password_confirm": "newpassword456"
}
```

**Response (200 OK):**

```json
{
  "message": "Password changed successfully. Please login again."
}
```

### 7. Get User Details

**GET** `/auth/api/user/`

Get detailed information about the current user (requires authentication).

**Headers:**

```
Authorization: Token your_auth_token_here
```

**Response (200 OK):**

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "phone_number": "+1234567890",
  "date_joined": "2023-10-10T10:30:00Z",
  "is_active": true
}
```

## Authentication

This API uses Token Authentication. After successful login or registration, you'll receive a token that must be included in the Authorization header for protected endpoints:

```
Authorization: Token your_auth_token_here
```

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

**400 Bad Request:**

```json
{
  "field_name": ["Error message for this field"],
  "non_field_errors": ["General error message"]
}
```

**401 Unauthorized:**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**

```json
{
  "detail": "You do not have permission to perform this action."
}
```

## Setup Instructions

1. Install required packages:

```bash
pip install djangorestframework djangorestframework-simplejwt
```

2. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

4. Start the development server:

```bash
python manage.py runserver
```

## Testing the API

You can test the API using tools like:

- Postman
- cURL
- DRF Browsable API (available when DEBUG=True)
- Python requests library

Example with cURL:

```bash
# Register a new user
curl -X POST http://localhost:8000/auth/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "phone_number": "1234567890",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'

# Login
curl -X POST http://localhost:8000/auth/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```
