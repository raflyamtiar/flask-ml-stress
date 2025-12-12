# Authentication & User Management API Documentation

API documentation untuk sistem autentikasi dan manajemen user menggunakan JWT (JSON Web Token).

## Base URL
```
http://localhost:5000
```

---

## 📋 Table of Contents
1. [Authentication Endpoints](#authentication-endpoints)
   - [Register](#1-register)
   - [Login](#2-login)
   - [Logout](#3-logout)
   - [Refresh Token](#4-refresh-token)
   - [Get Current User](#5-get-current-user)
2. [User Management Endpoints](#user-management-endpoints)
   - [Get All Users](#6-get-all-users)
   - [Get User by ID](#7-get-user-by-id)
   - [Update User](#8-update-user)
   - [Delete User](#9-delete-user)

---

## Authentication Endpoints

### 1. Register

Membuat user baru dalam sistem.

**Endpoint:** `POST /api/auth/register`

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "securePassword123"
}
```

**Success Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "johndoe",
    "email": "johndoe@example.com",
    "created_at": "2025-12-12T10:30:00+07:00",
    "updated_at": "2025-12-12T10:30:00+07:00"
  }
}
```

**Error Responses:**

- **400 Bad Request** (Missing fields):
```json
{
  "success": false,
  "error": "Username, email, and password are required"
}
```

- **400 Bad Request** (Username exists):
```json
{
  "success": false,
  "error": "Username already exists"
}
```

- **400 Bad Request** (Email exists):
```json
{
  "success": false,
  "error": "Email already exists"
}
```

---

### 2. Login

Autentikasi user dan mendapatkan JWT access & refresh token.

**Endpoint:** `POST /api/auth/login`

**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securePassword123"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "johndoe",
      "email": "johndoe@example.com",
      "created_at": "2025-12-12T10:30:00+07:00",
      "updated_at": "2025-12-12T10:30:00+07:00"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses:**

- **400 Bad Request** (Missing fields):
```json
{
  "success": false,
  "error": "Username and password are required"
}
```

- **401 Unauthorized** (Invalid credentials):
```json
{
  "success": false,
  "error": "Invalid username or password"
}
```

---

### 3. Logout

Logout user (client-side token removal).

**Endpoint:** `POST /api/auth/logout`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <access_token>"
}
```

**Request Body:**
```json
{}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

**Error Responses:**

- **401 Unauthorized** (Missing/Invalid token):
```json
{
  "msg": "Missing Authorization Header"
}
```

---

### 4. Refresh Token

Mendapatkan access token baru menggunakan refresh token.

**Endpoint:** `POST /api/auth/refresh`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <refresh_token>"
}
```

**Request Body:**
```json
{}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses:**

- **401 Unauthorized** (Missing/Invalid token):
```json
{
  "msg": "Missing Authorization Header"
}
```

- **422 Unprocessable Entity** (Access token used instead of refresh):
```json
{
  "msg": "Only refresh tokens are allowed"
}
```

---

### 5. Get Current User

Mendapatkan informasi user yang sedang login.

**Endpoint:** `GET /api/auth/me`

**Headers:**
```json
{
  "Authorization": "Bearer <access_token>"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "johndoe",
    "email": "johndoe@example.com",
    "created_at": "2025-12-12T10:30:00+07:00",
    "updated_at": "2025-12-12T10:30:00+07:00"
  }
}
```

**Error Responses:**

- **401 Unauthorized** (Missing/Invalid token):
```json
{
  "msg": "Missing Authorization Header"
}
```

- **404 Not Found** (User not found):
```json
{
  "success": false,
  "error": "User not found"
}
```

---

## User Management Endpoints

### 6. Get All Users

Mendapatkan list semua user (Protected endpoint).

**Endpoint:** `GET /api/users`

**Headers:**
```json
{
  "Authorization": "Bearer <access_token>"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "johndoe",
      "email": "johndoe@example.com",
      "created_at": "2025-12-12T10:30:00+07:00",
      "updated_at": "2025-12-12T10:30:00+07:00"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "username": "janedoe",
      "email": "janedoe@example.com",
      "created_at": "2025-12-12T11:00:00+07:00",
      "updated_at": "2025-12-12T11:00:00+07:00"
    }
  ]
}
```

**Error Responses:**

- **401 Unauthorized** (Missing/Invalid token):
```json
{
  "msg": "Missing Authorization Header"
}
```

---

### 7. Get User by ID

Mendapatkan informasi user berdasarkan ID (Protected endpoint).

**Endpoint:** `GET /api/users/<user_id>`

**Headers:**
```json
{
  "Authorization": "Bearer <access_token>"
}
```

**URL Parameters:**
- `user_id` (string, required): UUID dari user

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "johndoe",
    "email": "johndoe@example.com",
    "created_at": "2025-12-12T10:30:00+07:00",
    "updated_at": "2025-12-12T10:30:00+07:00"
  }
}
```

**Error Responses:**

- **401 Unauthorized** (Missing/Invalid token):
```json
{
  "msg": "Missing Authorization Header"
}
```

- **404 Not Found** (User not found):
```json
{
  "success": false,
  "error": "User not found"
}
```

---

### 8. Update User

Update informasi user (Protected endpoint).

**Endpoint:** `PUT /api/users/<user_id>`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <access_token>"
}
```

**URL Parameters:**
- `user_id` (string, required): UUID dari user

**Request Body:**
```json
{
  "username": "johndoe_updated",
  "email": "newemail@example.com",
  "password": "newSecurePassword123"
}
```

> **Note:** Semua field optional. Kirim hanya field yang ingin diupdate.

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "johndoe_updated",
    "email": "newemail@example.com",
    "created_at": "2025-12-12T10:30:00+07:00",
    "updated_at": "2025-12-12T14:20:00+07:00"
  }
}
```

**Error Responses:**

- **400 Bad Request** (No data provided):
```json
{
  "success": false,
  "error": "No data provided"
}
```

- **400 Bad Request** (Username exists):
```json
{
  "success": false,
  "error": "Username already exists"
}
```

- **400 Bad Request** (Email exists):
```json
{
  "success": false,
  "error": "Email already exists"
}
```

- **401 Unauthorized** (Missing/Invalid token):
```json
{
  "msg": "Missing Authorization Header"
}
```

- **404 Not Found** (User not found):
```json
{
  "success": false,
  "error": "User not found"
}
```

---

### 9. Delete User

Menghapus user dari sistem (Protected endpoint).

**Endpoint:** `DELETE /api/users/<user_id>`

**Headers:**
```json
{
  "Authorization": "Bearer <access_token>"
}
```

**URL Parameters:**
- `user_id` (string, required): UUID dari user

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

**Error Responses:**

- **401 Unauthorized** (Missing/Invalid token):
```json
{
  "msg": "Missing Authorization Header"
}
```

- **404 Not Found** (User not found):
```json
{
  "success": false,
  "error": "User not found"
}
```

---

## 🔐 Token Information

### Access Token
- **Expiration:** 1 hour (3600 seconds)
- **Usage:** Digunakan untuk mengakses protected endpoints
- **Header Format:** `Authorization: Bearer <access_token>`

### Refresh Token
- **Expiration:** 30 days (2592000 seconds)
- **Usage:** Digunakan untuk mendapatkan access token baru
- **Header Format:** `Authorization: Bearer <refresh_token>`

---

## 📝 Postman Testing Guide

### Step 1: Register User
1. Method: `POST`
2. URL: `http://localhost:5000/api/auth/register`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

### Step 2: Login
1. Method: `POST`
2. URL: `http://localhost:5000/api/auth/login`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "username": "testuser",
  "password": "password123"
}
```
5. **Save `access_token` dari response untuk request selanjutnya**

### Step 3: Get Current User (Protected)
1. Method: `GET`
2. URL: `http://localhost:5000/api/auth/me`
3. Headers:
   - `Authorization: Bearer <paste_access_token_here>`

### Step 4: Update User (Protected)
1. Method: `PUT`
2. URL: `http://localhost:5000/api/users/<user_id>`
3. Headers:
   - `Content-Type: application/json`
   - `Authorization: Bearer <paste_access_token_here>`
4. Body (raw JSON):
```json
{
  "username": "testuser_updated"
}
```

### Step 5: Get All Users (Protected)
1. Method: `GET`
2. URL: `http://localhost:5000/api/users`
3. Headers:
   - `Authorization: Bearer <paste_access_token_here>`

---

## ⚠️ Important Notes

1. **Password Security:** Password di-hash menggunakan Werkzeug security (bcrypt compatible)
2. **JWT Secret:** Pastikan set `JWT_SECRET_KEY` di environment variables untuk production
3. **Token Expiration:** Access token expire dalam 1 jam, gunakan refresh token untuk mendapatkan token baru
4. **Protected Endpoints:** Semua endpoint di `/api/users/*` dan `/api/auth/me`, `/api/auth/logout`, `/api/auth/refresh` memerlukan JWT token
5. **User ID Format:** Menggunakan UUID v4 format
6. **Timezone:** Semua timestamp menggunakan Jakarta timezone (UTC+7)

---

## 🚀 Quick Start with cURL

### Register:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

### Login:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

### Get Current User:
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🔄 Migration Commands

Sebelum menggunakan API, pastikan database sudah di-migrate:

```bash
# Set Flask app
$env:FLASK_APP="run.py"

# Create migration
flask db migrate -m "Add User table for authentication"

# Apply migration
flask db upgrade
```

---

## ✅ Testing Checklist

- [ ] Register user baru
- [ ] Login dengan credentials yang benar
- [ ] Login dengan credentials yang salah (test error handling)
- [ ] Get current user info dengan valid token
- [ ] Get current user info tanpa token (test auth)
- [ ] Update user profile
- [ ] Get all users
- [ ] Get user by ID
- [ ] Delete user
- [ ] Refresh access token
- [ ] Logout

---

**Happy Testing! 🎉**
