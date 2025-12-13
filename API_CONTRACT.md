# API Contract Documentation

Dokumentasi lengkap API contract untuk Flask ML Stress Detection System.

**Base URL:** `http://127.0.0.1:5000`

**Authentication:** JWT Bearer Token (untuk endpoint yang memerlukan auth)

**Version:** 2.2.0

**Last Updated:** December 13, 2025

---

## 📑 Table of Contents

1. [API Status](#api-status)
2. [Authentication & Users](#authentication--users)
3. [App Info](#app-info)
4. [Measurement Sessions](#measurement-sessions)
5. [Sensor Readings](#sensor-readings)
6. [Stress History](#stress-history)
7. [ML Prediction](#ml-prediction)
8. [WebSocket & ESP32](#websocket--esp32)
9. [System Status](#system-status)
10. [Error Responses](#error-responses)

---

## API Status

### Check API Status

**Endpoint:** `GET /api`

**Auth Required:** No

**Description:** Simple endpoint to check if API is running.

**Success Response (200):**

```json
{
  "success": true,
  "status": "ok",
  "message": "API is running"
}
```

**Example:**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api" -Method GET
```

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
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "uuid-string",
      "username": "john_doe",
      "email": "john@example.com"
    }
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

**Error Response (400):**

```json
{
  "success": false,
  "error": "Username and password are required"
}
```

---

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

````

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
````

---

### Logout

**Endpoint:** `POST /api/auth/logout`

**Auth Required:** Yes

**Headers:**

```
Authorization: Bearer <access_token>
```

**Description:** Logout endpoint (actual token removal is handled client-side).

**Success Response (200):**

```json
{
  "success": true,
  "message": "Logout successful"
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
  "message": "User updated successfully",
  "data": {
    "id": "uuid-string",
    "username": "john_updated",
    "email": "john_updated@example.com",
    "updated_at": "2025-12-12T11:00:00+07:00"
  }
}
```

**Error Response (400):**

```json
{
  "success": false,
  "error": "No data provided"
}
```

**Error Response (404):**

```json
{
  "success": false,
  "error": "User not found"
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

**Error Response (404):**

```json
{
  "success": false,
  "error": "User not found"
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
      "name": "Morning Session",
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
    "name": "Morning Session",
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
  "name": "string (optional, max 255 characters)",
  "notes": "string (optional)"
}
```

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "id": "new-uuid-here",
    "name": "Afternoon Session",
    "created_at": "2025-12-12T15:00:00+07:00",
    "notes": "Afternoon session"
  }
}
```

**Example:**

```powershell
$body = @{
  name = "Evening Workout Session"
  notes = "After gym measurement"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/sessions" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

---

### Update Session

**Endpoint:** `PUT /api/sessions/{session_id}`

**Auth Required:** Yes 🔐

**Headers:**

```
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
  "name": "string (optional, max 255 characters)",
  "notes": "string (optional)"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "Updated Session Name",
    "created_at": "2025-12-12T15:00:00+07:00",
    "notes": "Updated notes"
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

**Error Response (400):**

```json
{
  "success": false,
  "error": "No data provided"
}
```

**Example:**

```powershell
$headers = @{
  "Authorization" = "Bearer $token"
}

$body = @{
  name = "Updated Morning Session"
  notes = "Updated measurement notes"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/sessions/$sessionId" `
  -Method PUT `
  -Headers $headers `
  -ContentType "application/json" `
  -Body $body
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

**Error Response (404):**

```json
{
  "success": false,
  "error": "Session not found"
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

**Error Response (400):**

```json
{
  "success": false,
  "error": "Missing fields: session_id, hr, temp, eda"
}
```

---

### Bulk Create Sensor Readings

**Endpoint:** `POST /api/sessions/{session_id}/sensor-readings/bulk`

**Auth Required:** No

**Description:** Create multiple sensor readings for a specific session at once.

**Request Body:**

```json
{
  "readings": [
    {
      "hr": 75.0,
      "temp": 36.8,
      "eda": 0.45
    },
    {
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
  "created_count": 2,
  "error_count": 0,
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

**Partial Success Response (201):**

```json
{
  "success": true,
  "created_count": 1,
  "error_count": 1,
  "data": [
    {
      "id": 10,
      "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "hr": 75.0,
      "temp": 36.8,
      "eda": 0.45
    }
  ],
  "errors": [
    {
      "index": 1,
      "error": "Missing fields: hr"
    }
  ]
}
```

**Error Response (400):**

```json
{
  "success": false,
  "error": "Request body must contain \"readings\" array"
}
```

```json
{
  "success": false,
  "error": "Readings array cannot be empty"
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

**Error Response (404):**

```json
{
  "success": false,
  "error": "Reading not found"
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

**Error Response (404):**

```json
{
  "success": false,
  "error": "Reading not found"
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
  "hr": "float (required)",
  "temp": "float (required)",
  "eda": "float (required)",
  "label": "string (required: Normal, Medium, High Stress)",
  "confidence_level": "float (optional, 0.0-1.0)",
  "notes": "string (optional)"
}
```

**Note:** `timestamp` is automatically set by the service if not provided.

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

**Auth Required:** Yes 🔐

**Headers:**

```
Authorization: Bearer <access_token>
```

**Request Body:**

```json
{
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

**Error Response (404):**

```json
{
  "success": false,
  "error": "Record not found"
}
```

---

### Delete Stress History

**Endpoint:** `DELETE /api/stress-history/{id}`

**Auth Required:** Yes 🔐

**Headers:**

```
Authorization: Bearer <access_token>
```

**⚠️ WARNING - CASCADE DELETE:** Deleting a stress history record will **cascade delete the entire measurement session**, including:

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

**Error Response (404):**

```json
{
  "success": false,
  "error": "Record not found"
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
  "data": {
    "hr": 75.0,
    "temp": 36.8,
    "eda": 0.45,
    "label": "Normal",
    "confidence_level": 0.95
  },
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "history_id": 123,
  "sensor_reading_id": 456
}
```

**Error Response (400):**

```json
{
  "success": false,
  "error": "Missing fields: hr, temp, eda"
}
```

```json
{
  "success": false,
  "error": "hr, temp and eda must be numbers"
}
```

**Possible Labels:**

- `Normal` - No stress detected
- `Medium` - Moderate stress level
- `High Stress` - High stress level

**Example:**

```powershell
$body = @{
  hr = 75.0
  temp = 36.8
  eda = 0.45
  notes = "Morning measurement"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/predict-stress" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

---

## WebSocket & ESP32

### Get WebSocket Info

**Endpoint:** `GET /api/websocket/info`

**Auth Required:** No

**Description:** Get WebSocket connection information, available events, and data formats.

**Success Response (200):**

```json
{
  "success": true,
  "websocket_url": "/socket.io/",
  "events": {
    "esp32": {
      "connect_params": "?type=esp32",
      "send_data_event": "esp32_sensor_data",
      "data_format": {
        "hr": "float - heart rate",
        "temp": "float - temperature in celsius",
        "eda": "float - electrodermal activity",
        "timestamp": "string/int - ISO format or unix timestamp (optional)",
        "device_id": "string - device identifier (optional)"
      }
    },
    "frontend": {
      "connect_params": "?type=frontend",
      "listen_events": ["new_sensor_data", "stress_alert", "client_stats"],
      "send_events": [
        "frontend_request_history",
        "frontend_subscribe_alerts",
        "ping"
      ]
    }
  },
  "example_urls": {
    "esp32_connection": "http://127.0.0.1:5000/socket.io/?type=esp32",
    "frontend_connection": "http://127.0.0.1:5000/socket.io/?type=frontend"
  }
}
```

---

### WebSocket Test Page

**Endpoint:** `GET /api/websocket/test`

**Auth Required:** No

**Description:** Serve a simple WebSocket test page for testing connections.

**Returns:** HTML page for WebSocket testing

---

### ESP32 HTTP Fallback

**Endpoint:** `POST /api/esp32/data`

**Auth Required:** No

**Description:** HTTP fallback endpoint for ESP32 if WebSocket is not available. Performs stress prediction and saves data.

**Request Body:**

```json
{
  "hr": "float (required, heart rate)",
  "temp": "float (required, temperature in celsius)",
  "eda": "float (required, electrodermal activity)",
  "timestamp": "string/int (optional, ISO format or unix timestamp)",
  "device_id": "string (optional, device identifier)"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "message": "Data received and processed successfully",
  "data": {
    "record_id": 123,
    "timestamp": "2025-12-12T14:30:00+07:00",
    "stress_prediction": {
      "label": "Normal",
      "confidence": 95.5
    },
    "sensor_data": {
      "hr": 75.0,
      "temp": 36.8,
      "eda": 0.45
    }
  },
  "note": "For real-time updates, use WebSocket connection at /socket.io/?type=esp32"
}
```

**Error Response (400):**

```json
{
  "success": false,
  "error": "No JSON data provided"
}
```

```json
{
  "success": false,
  "error": "Missing required fields: hr, temp, eda"
}
```

```json
{
  "success": false,
  "error": "hr, temp, and eda must be valid numbers"
}
```

**Example:**

```powershell
$body = @{
  hr = 75.0
  temp = 36.8
  eda = 0.45
  device_id = "ESP32_001"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/esp32/data" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

---

## System Status

### Get System Status

**Endpoint:** `GET /api/system/status`

**Auth Required:** No

**Description:** Get system status including WebSocket connections, statistics, and available features.

**Success Response (200):**

```json
{
  "success": true,
  "status": "running",
  "features": {
    "websocket": true,
    "http_api": true,
    "stress_prediction": true,
    "real_time_monitoring": true
  },
  "statistics": {
    "total_records": 1250,
    "recent_24h_records": 85,
    "last_updated": "2025-12-12T16:30:00+07:00"
  },
  "endpoints": {
    "websocket": "/socket.io/",
    "http_esp32_fallback": "/api/esp32/data",
    "websocket_info": "/api/websocket/info",
    "system_status": "/api/system/status"
  }
}
```

**Error Response (500):**

```json
{
  "success": false,
  "status": "error",
  "error": "Error message here"
}
```

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
- Timestamps are automatically generated by the service if not provided

### UUIDs

- Session IDs use UUID v4 format
- User IDs use UUID v4 format
- Example: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`

### Authentication

- JWT tokens expire after configured time (default: 15 minutes for access token)
- Refresh tokens have longer expiration (default: 30 days)
- Include token in `Authorization` header: `Bearer <token>`
- Use `/api/auth/refresh` endpoint to get new access token

### Cascade Delete Behavior

**⚠️ IMPORTANT: Understand cascade delete before deleting records**

**Session → Related Data:**

- Deleting a `measurement_session` removes all related `sensor_readings` and `stress_history`

**Stress History → Session:**

- Deleting a `stress_history` record removes its associated `measurement_session`
- This triggers the above cascade, removing all data for that session

### Data Validation

- All numeric fields (hr, temp, eda) must be valid numbers
- Email addresses must be in valid format
- Passwords must be at least 6 characters
- Username and email must be unique

### WebSocket Integration

- Real-time data streaming available via Socket.IO
- Two connection types: `esp32` and `frontend`
- HTTP fallback available at `/api/esp32/data`
- See [WEBSOCKET_GUIDE.md](WEBSOCKET_GUIDE.md) for detailed WebSocket documentation

---

## Example Usage

### PowerShell Examples

**Check API Status:**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api" -Method GET
```

**Register User:**

```powershell
$body = @{
  username = "john_doe"
  email = "john@example.com"
  password = "secure123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/register" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**Login:**

```powershell
$body = @{
  username = "john_doe"
  password = "secure123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body

$token = $response.data.access_token
```

**Get Current User:**

```powershell
$headers = @{
  "Authorization" = "Bearer $token"
}

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/me" `
  -Method GET `
  -Headers $headers
```

**Create Session:**

```powershell
$body = @{
  notes = "Morning session"
} | ConvertTo-Json

$session = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/sessions" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body

$sessionId = $session.data.id
```

**Bulk Create Sensor Readings:**

```powershell
$body = @{
  readings = @(
    @{ hr = 75.0; temp = 36.8; eda = 0.45 },
    @{ hr = 76.0; temp = 36.9; eda = 0.47 },
    @{ hr = 77.0; temp = 37.0; eda = 0.48 }
  )
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/sessions/$sessionId/sensor-readings/bulk" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**Predict Stress:**

```powershell
$body = @{
  hr = 85.0
  temp = 37.2
  eda = 0.68
  notes = "After exercise"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/predict-stress" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**Get System Status:**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/system/status" -Method GET
```

**Delete Session with Auth:**

```powershell
$headers = @{
  "Authorization" = "Bearer $token"
}

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/sessions/$sessionId" `
  -Method DELETE `
  -Headers $headers
```

---

## Related Documentation

- **[AUTH_API.md](AUTH_API.md)** - Detailed authentication flow and JWT implementation
- **[WEBSOCKET_GUIDE.md](WEBSOCKET_GUIDE.md)** - WebSocket real-time communication guide
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - API testing guide and examples
- **[README.md](README.md)** - Project overview and setup instructions

---

**Version:** 2.2.0  
**Last Updated:** December 13, 2025  
**Maintained by:** Flask ML Stress Detection Team
