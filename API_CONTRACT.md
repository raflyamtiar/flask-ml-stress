# API Contract Documentation

Dokumentasi lengkap API contract untuk Flask ML Stress Detection System.

**Base URL:** `http://127.0.0.1:5000`

**Authentication:** JWT Bearer Token (untuk endpoint yang memerlukan auth)

---

## 📑 Table of Contents

1. [Authentication & Users](#authentication--users)
2. [App Info](#app-info)
3. [Measurement Sessions](#measurement-sessions)
4. [Sensor Readings](#sensor-readings)
5. [Stress History](#stress-history)
6. [ML Prediction](#ml-prediction)
7. [Error Responses](#error-responses)

---

## Authentication & Users

### Register User

**Endpoint:** `POST /api/auth/register`

**Auth Required:** No

**Request Body:**

```json
{
  "username": "string (required, unique)",
  "email": "string (required, unique, valid email)",
  "password": "string (required, min 6 characters)"
}
```

**Success Response (201):**

```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": "uuid-string",
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2025-12-12T10:30:00+07:00"
  }
}
```

**Error Response (400):**

```json
{
  "success": false,
  "error": "Username already exists"
}
```

---

### Login

**Endpoint:** `POST /api/auth/login`

**Auth Required:** No

**Request Body:**

```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid-string",
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

**Error Response (401):**

```json
{
  "success": false,
  "error": "Invalid username or password"
}
```

---

### Refresh Token

**Endpoint:** `POST /api/auth/refresh`

**Auth Required:** Yes (Refresh Token)

**Headers:**

```
Authorization: Bearer <refresh_token>
```

**Success Response (200):**

```json
{
  "success": true,
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Get Current User

**Endpoint:** `GET /api/auth/me`

**Auth Required:** Yes

**Headers:**

```
Authorization: Bearer <access_token>
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2025-12-12T10:30:00+07:00",
    "updated_at": "2025-12-12T10:30:00+07:00"
  }
}
```

---

### Get All Users

**Endpoint:** `GET /api/users`

**Auth Required:** Yes

**Headers:**

```
Authorization: Bearer <access_token>
```

**Success Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid-string",
      "username": "john_doe",
      "email": "john@example.com",
      "created_at": "2025-12-12T10:30:00+07:00"
    }
  ]
}
```

---

### Update User

**Endpoint:** `PUT /api/users/{user_id}`

**Auth Required:** Yes

**Headers:**

```
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "username": "string (optional)",
  "email": "string (optional)",
  "password": "string (optional)"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": "uuid-string",
    "username": "john_updated",
    "email": "john_updated@example.com",
    "updated_at": "2025-12-12T11:00:00+07:00"
  }
}
```

---

### Delete User

**Endpoint:** `DELETE /api/users/{user_id}`

**Auth Required:** Yes

**Headers:**

```
Authorization: Bearer <access_token>
```

**Success Response (200):**

```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

---

## App Info

### Get All App Info

**Endpoint:** `GET /api/app-info`

**Auth Required:** No

**Success Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "app_name": "Stress Detection System",
      "app_version": "2.2.0",
      "description": "Real-time stress monitoring system",
      "owner": "Team XYZ",
      "contact": "admin@example.com",
      "created_at": "2025-12-01T08:00:00+07:00",
      "updated_at": "2025-12-12T10:00:00+07:00"
    }
  ]
}
```

---

### Get App Info by ID

**Endpoint:** `GET /api/app-info/{id}`

**Auth Required:** No

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "app_name": "Stress Detection System",
    "app_version": "2.2.0",
    "description": "Real-time stress monitoring system",
    "owner": "Team XYZ",
    "contact": "admin@example.com",
    "created_at": "2025-12-01T08:00:00+07:00",
    "updated_at": "2025-12-12T10:00:00+07:00"
  }
}
```

**Error Response (404):**

```json
{
  "success": false,
  "error": "App info not found"
}
```

---

### Create App Info

**Endpoint:** `POST /api/app-info`

**Auth Required:** No

**Request Body:**

```json
{
  "app_name": "string (required)",
  "app_version": "string (optional)",
  "description": "string (optional)",
  "owner": "string (optional)",
  "contact": "string (optional)"
}
```

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "id": 2,
    "app_name": "New App",
    "app_version": "1.0.0",
    "description": "Description here",
    "owner": "Owner Name",
    "contact": "contact@example.com",
    "created_at": "2025-12-12T12:00:00+07:00",
    "updated_at": "2025-12-12T12:00:00+07:00"
  }
}
```

---

### Update App Info

**Endpoint:** `PUT /api/app-info/{id}`

**Auth Required:** Yes 🔐

**Headers:**

```
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "app_name": "string (optional)",
  "app_version": "string (optional)",
  "description": "string (optional)",
  "owner": "string (optional)",
  "contact": "string (optional)"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "app_name": "Updated Name",
    "app_version": "2.3.0",
    "updated_at": "2025-12-12T13:00:00+07:00"
  }
}
```

---

### Delete App Info

**Endpoint:** `DELETE /api/app-info/{id}`

**Auth Required:** Yes 🔐

**Headers:**

```
Authorization: Bearer <access_token>
```

**Success Response (200):**

```json
{
  "success": true,
  "message": "App info deleted successfully"
}
```

---

## Measurement Sessions

### Get All Sessions

**Endpoint:** `GET /api/sessions`

**Auth Required:** No

**Success Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "created_at": "2025-12-12T14:30:00+07:00",
      "notes": "Morning measurement"
    }
  ]
}
```

---

### Get Session by ID

**Endpoint:** `GET /api/sessions/{session_id}`

**Auth Required:** No

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "created_at": "2025-12-12T14:30:00+07:00",
    "notes": "Morning measurement"
  }
}
```

**Error Response (404):**

```json
{
  "success": false,
  "error": "Session not found"
}
```

---

### Create Session

**Endpoint:** `POST /api/sessions`

**Auth Required:** No

**Request Body:**

```json
{
  "notes": "string (optional)"
}
```

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "id": "new-uuid-here",
    "created_at": "2025-12-12T15:00:00+07:00",
    "notes": "Afternoon session"
  }
}
```

---

### Delete Session

**Endpoint:** `DELETE /api/sessions/{session_id}`

**Auth Required:** Yes 🔐

**Headers:**

```
Authorization: Bearer <access_token>
```

**⚠️ CASCADE DELETE:** This will delete all related `sensor_readings` and `stress_history` records.

**Success Response (200):**

```json
{
  "success": true,
  "message": "Session deleted"
}
```

---

### Get Stress History by Session

**Endpoint:** `GET /api/sessions/{session_id}/stress-history`

**Auth Required:** No

**Success Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": 10,
      "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "timestamp": "2025-12-12T14:35:00+07:00",
      "hr": 75.5,
      "temp": 36.8,
      "eda": 0.45,
      "label": "Normal",
      "confidence_level": 0.92,
      "notes": "",
      "created_at": "2025-12-12T14:35:10+07:00"
    }
  ]
}
```

---

### Get Sensor Readings by Session

**Endpoint:** `GET /api/sessions/{session_id}/sensor-readings`

**Auth Required:** No

**Success Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": 25,
      "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "timestamp": "2025-12-12T14:30:15+07:00",
      "hr": 75.0,
      "temp": 36.7,
      "eda": 0.42,
      "created_at": "2025-12-12T14:30:16+07:00"
    }
  ]
}
```

---

## Sensor Readings

### Get All Sensor Readings

**Endpoint:** `GET /api/sensor-readings`

**Auth Required:** No

**Success Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "timestamp": "2025-12-12T14:30:00+07:00",
      "hr": 75.0,
      "temp": 36.8,
      "eda": 0.45,
      "created_at": "2025-12-12T14:30:01+07:00"
    }
  ]
}
```

---

### Get Sensor Reading by ID

**Endpoint:** `GET /api/sensor-readings/{id}`

**Auth Required:** No

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "timestamp": "2025-12-12T14:30:00+07:00",
    "hr": 75.0,
    "temp": 36.8,
    "eda": 0.45,
    "created_at": "2025-12-12T14:30:01+07:00"
  }
}
```

---

### Create Sensor Reading

**Endpoint:** `POST /api/sensor-readings`

**Auth Required:** No

**Request Body:**

```json
{
  "session_id": "string (required, UUID)",
  "timestamp": "string (required, ISO 8601 datetime)",
  "hr": "float (required, heart rate)",
  "temp": "float (required, temperature in celsius)",
  "eda": "float (required, electrodermal activity)"
}
```

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "id": 2,
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "timestamp": "2025-12-12T14:35:00+07:00",
    "hr": 78.5,
    "temp": 37.0,
    "eda": 0.5,
    "created_at": "2025-12-12T14:35:02+07:00"
  }
}
```

---

### Bulk Create Sensor Readings

**Endpoint:** `POST /api/sessions/{session_id}/sensor-readings/bulk`

**Auth Required:** No

**Request Body:**

```json
{
  "readings": [
    {
      "timestamp": "2025-12-12T14:30:00+07:00",
      "hr": 75.0,
      "temp": 36.8,
      "eda": 0.45
    },
    {
      "timestamp": "2025-12-12T14:30:05+07:00",
      "hr": 76.0,
      "temp": 36.9,
      "eda": 0.47
    }
  ]
}
```

**Success Response (201):**

```json
{
  "success": true,
  "message": "2 readings created",
  "data": [
    {
      "id": 10,
      "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "timestamp": "2025-12-12T14:30:00+07:00",
      "hr": 75.0,
      "temp": 36.8,
      "eda": 0.45,
      "created_at": "2025-12-12T14:30:01+07:00"
    },
    {
      "id": 11,
      "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "timestamp": "2025-12-12T14:30:05+07:00",
      "hr": 76.0,
      "temp": 36.9,
      "eda": 0.47,
      "created_at": "2025-12-12T14:30:06+07:00"
    }
  ]
}
```

---

### Update Sensor Reading

**Endpoint:** `PUT /api/sensor-readings/{id}`

**Auth Required:** Yes 🔐

**Headers:**

```
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "timestamp": "string (optional)",
  "hr": "float (optional)",
  "temp": "float (optional)",
  "eda": "float (optional)"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "timestamp": "2025-12-12T14:30:00+07:00",
    "hr": 80.0,
    "temp": 37.2,
    "eda": 0.55,
    "created_at": "2025-12-12T14:30:01+07:00"
  }
}
```

---

### Delete Sensor Reading

**Endpoint:** `DELETE /api/sensor-readings/{id}`

**Auth Required:** Yes 🔐

**Headers:**

```
Authorization: Bearer <access_token>
```

**Success Response (200):**

```json
{
  "success": true,
  "message": "Reading deleted"
}
```

---

## Stress History

### Get All Stress History

**Endpoint:** `GET /api/stress-history`

**Auth Required:** No

**Success Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "timestamp": "2025-12-12T14:35:00+07:00",
      "hr": 82.0,
      "temp": 37.1,
      "eda": 0.68,
      "label": "Medium",
      "confidence_level": 0.87,
      "notes": "Slightly elevated stress",
      "created_at": "2025-12-12T14:35:05+07:00"
    }
  ]
}
```

---

### Get Stress History by ID

**Endpoint:** `GET /api/stress-history/{id}`

**Auth Required:** No

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "timestamp": "2025-12-12T14:35:00+07:00",
    "hr": 82.0,
    "temp": 37.1,
    "eda": 0.68,
    "label": "Medium",
    "confidence_level": 0.87,
    "notes": "Slightly elevated stress",
    "created_at": "2025-12-12T14:35:05+07:00"
  }
}
```

---

### Create Stress History

**Endpoint:** `POST /api/stress-history`

**Auth Required:** No

**Request Body:**

```json
{
  "session_id": "string (optional, UUID)",
  "timestamp": "string (required, ISO 8601 datetime)",
  "hr": "float (required)",
  "temp": "float (required)",
  "eda": "float (required)",
  "label": "string (required: Normal, Medium, High Stress)",
  "confidence_level": "float (optional, 0.0-1.0)",
  "notes": "string (optional)"
}
```

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "id": 2,
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "timestamp": "2025-12-12T15:00:00+07:00",
    "hr": 75.0,
    "temp": 36.8,
    "eda": 0.45,
    "label": "Normal",
    "confidence_level": 0.95,
    "notes": "Relaxed state",
    "created_at": "2025-12-12T15:00:02+07:00"
  }
}
```

---

### Update Stress History

**Endpoint:** `PUT /api/stress-history/{id}`

**Auth Required:** No

**Request Body:**

```json
{
  "timestamp": "string (optional)",
  "hr": "float (optional)",
  "temp": "float (optional)",
  "eda": "float (optional)",
  "label": "string (optional)",
  "confidence_level": "float (optional)",
  "notes": "string (optional)"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": 1,
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "timestamp": "2025-12-12T14:35:00+07:00",
    "hr": 82.0,
    "temp": 37.1,
    "eda": 0.68,
    "label": "Medium",
    "confidence_level": 0.87,
    "notes": "Updated notes",
    "created_at": "2025-12-12T14:35:05+07:00"
  }
}
```

---

### Delete Stress History

**Endpoint:** `DELETE /api/stress-history/{id}`

**Auth Required:** No

**⚠️ CRITICAL CASCADE DELETE:** Deleting a stress history record will **automatically delete its entire measurement session**, including:

- The associated `measurement_session`
- ALL `stress_history` records with the same `session_id`
- ALL `sensor_readings` with the same `session_id`

This action **cannot be undone**.

**Success Response (200):**

```json
{
  "success": true,
  "message": "Record deleted"
}
```

---

## ML Prediction

### Predict Stress

**Endpoint:** `POST /api/predict-stress`

**Auth Required:** No

**Description:** Predicts stress level using ML model. Automatically creates a measurement session and saves both sensor readings and prediction results.

**Request Body:**

```json
{
  "hr": "float (required, heart rate in BPM)",
  "temp": "float (required, temperature in celsius)",
  "eda": "float (required, electrodermal activity)",
  "notes": "string (optional)"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "prediction": {
    "label": "Normal",
    "confidence": 0.95,
    "session_id": "new-uuid-here"
  },
  "sensor_data": {
    "hr": 75.0,
    "temp": 36.8,
    "eda": 0.45
  },
  "timestamp": "2025-12-12T16:00:00+07:00"
}
```

**Possible Labels:**

- `Normal` - No stress detected
- `Medium` - Moderate stress level
- `High Stress` - High stress level

---

## Error Responses

### Common Error Codes

**400 Bad Request:**

```json
{
  "success": false,
  "error": "Validation error message"
}
```

**401 Unauthorized:**

```json
{
  "msg": "Missing Authorization Header"
}
```

**404 Not Found:**

```json
{
  "success": false,
  "error": "Resource not found"
}
```

**500 Internal Server Error:**

```json
{
  "success": false,
  "error": "Internal server error message"
}
```

---

## Notes

### Timestamps

- All timestamps are in **Jakarta timezone (UTC+7)**
- Format: ISO 8601 (e.g., `2025-12-12T14:30:00+07:00`)

### UUIDs

- Session IDs use UUID v4 format
- User IDs use UUID v4 format
- Example: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`

### Authentication

- JWT tokens expire after configured time (default: 15 minutes for access token)
- Refresh tokens have longer expiration
- Include token in `Authorization` header: `Bearer <token>`

### Cascade Delete Behavior

**Session → Related Data:**

- Deleting a `measurement_session` removes all related `sensor_readings` and `stress_history`

**Stress History → Session:**

- Deleting a `stress_history` record removes its associated `measurement_session`
- This triggers the above cascade, removing all data for that session

---

## Example Usage

### PowerShell Examples

**Login:**

```powershell
$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"username":"admin","password":"password123"}'

$token = $response.access_token
```

**Create Session with Auth:**

```powershell
$headers = @{
  "Authorization" = "Bearer $token"
  "Content-Type" = "application/json"
}

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/sessions/uuid-here" `
  -Method DELETE `
  -Headers $headers
```

**Predict Stress:**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/predict-stress" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"hr":75.0,"temp":36.8,"eda":0.45}'
```

---

**Version:** 2.2.0  
**Last Updated:** December 12, 2025
