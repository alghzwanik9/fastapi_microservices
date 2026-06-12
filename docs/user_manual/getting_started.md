# User Manual - Microservices Platform

## Introduction

Welcome to the Microservices Platform! This guide will help you understand and use the system effectively.

## Table of Contents

1. [Getting Started](#getting-started)
2. [User Registration](#user-registration)
3. [Authentication](#authentication)
4. [Managing Your Profile](#managing-your-profile)
5. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Accessing the API

The platform provides REST APIs for all operations. You can interact with the API using:
- **cURL** (command line)
- **Postman** (GUI client)
- **Any HTTP client library** (Python, JavaScript, etc.)

**Base URL**: `http://localhost:8001/api/v1`

---

## User Registration

To create a new account, send a POST request to the register endpoint:

### Example using cURL:
```bash
curl -X POST http://localhost:8001/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "password": "securepassword123"
  }'
```

### Example using Python:
```python
import requests

response = requests.post(
    "http://localhost:8001/api/v1/users/register",
    json={
        "email": "john@example.com",
        "username": "johndoe",
        "full_name": "John Doe",
        "password": "securepassword123"
    }
)

print(response.json())
```

### Requirements:
- **Email**: Must be a valid email format
- **Username**: 3-50 characters
- **Password**: Minimum 8 characters

---

## Authentication

After registration, you need to login to get an access token:

### Login Request:
```bash
curl -X POST http://localhost:8001/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

### Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using the Token:
Include the token in all authenticated requests:

```bash
curl -X GET http://localhost:8001/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Managing Your Profile

### View Your Profile:
```bash
curl -X GET http://localhost:8001/api/v1/users/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Your Profile:
```bash
curl -X PUT http://localhost:8001/api/v1/users/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Smith",
    "email": "newemail@example.com"
  }'
```

### Delete Your Account:
```bash
curl -X DELETE http://localhost:8001/api/v1/users/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

⚠️ **Warning**: This action is permanent and cannot be undone!

---

## Troubleshooting

### Common Errors:

#### 400 Bad Request
- **Email already registered**: Choose a different email
- **Username already taken**: Choose a different username
- **Inactive user**: Contact support to activate your account

#### 401 Unauthorized
- **Invalid credentials**: Check your username and password
- **Token expired**: Login again to get a new token
- **Invalid token format**: Ensure you're using "Bearer " prefix

#### 404 Not Found
- **User not found**: The requested user ID doesn't exist

#### 422 Validation Error
- **Password too short**: Use at least 8 characters
- **Invalid email format**: Use a valid email address

### Getting Help:

1. Check the API documentation at `/docs` (Swagger UI)
2. Review error messages in the response body
3. Contact support at support@example.com

---

## Security Best Practices

1. **Never share your password** or access token
2. **Use strong passwords** with a mix of letters, numbers, and symbols
3. **Logout** when you're done (don't keep tokens indefinitely)
4. **Enable HTTPS** in production environments
5. **Rotate secrets** regularly

---

## API Rate Limits

- **Unauthenticated requests**: 10 requests per minute
- **Authenticated requests**: 100 requests per minute

If you exceed the limit, you'll receive a 429 Too Many Requests error.
