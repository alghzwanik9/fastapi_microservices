# User Service API Documentation

## Base URL
```
http://localhost:8001/api/v1
```

## Authentication

Most endpoints require authentication using JWT Bearer tokens.

### Login
**Endpoint**: `POST /users/login`

**Request Body**:
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using the Token
Include the token in the Authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Endpoints

### Register User
**Endpoint**: `POST /users/register`

**Authentication**: Not required

**Request Body**:
```json
{
  "email": "john@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "password": "securepassword123"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### Get Current User
**Endpoint**: `GET /users/me`

**Authentication**: Required

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### Get User by ID
**Endpoint**: `GET /users/{user_id}`

**Authentication**: Required

**Path Parameters**:
- `user_id` (integer): The ID of the user

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

### Update User
**Endpoint**: `PUT /users/{user_id}`

**Authentication**: Required

**Path Parameters**:
- `user_id` (integer): The ID of the user

**Request Body** (all fields optional):
```json
{
  "email": "newemail@example.com",
  "username": "newusername",
  "full_name": "New Name",
  "password": "newpassword123",
  "is_active": true
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "newemail@example.com",
  "username": "newusername",
  "full_name": "New Name",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

---

### Delete User
**Endpoint**: `DELETE /users/{user_id}`

**Authentication**: Required

**Path Parameters**:
- `user_id` (integer): The ID of the user

**Response** (204 No Content)

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "ensure this value has at least 8 characters",
      "type": "value_error.any_str.min_length",
      "ctx": {"limit_value": 8}
    }
  ]
}
```

---

## Health Check
**Endpoint**: `GET /health`

**Authentication**: Not required

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "user-service"
}
```
