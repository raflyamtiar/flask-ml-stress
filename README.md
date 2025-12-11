# Flask Stress App - Real-time Monitoring System

Flask application for real-time stress monitoring with WebSocket support for ESP32 devices and React frontend.

## Quick start (PowerShell)

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = 'run.py'
flask run
```

Open http://127.0.0.1:5000/ in your browser.

## Notes

- Secrets like `SECRET_KEY` should be set via environment variables or `instance/config.py`.
- `app/__init__.py` provides `create_app()` factory for easy testing and configuration.

## Local environment

Copy `.env.example` to `.env` and edit values for local development, or set corresponding environment variables.

Example (PowerShell):

```powershell
Copy-Item .env.example .env
$env:SECRET_KEY = 'your-secret'
```

## Using the setup script

Run the `setup.ps1` script from the project root to create and populate the virtual environment and to create an `instance/app.db` SQLite file if missing.

To run the script (no persistent activation):

```powershell
.\setup.ps1
```

To run and keep the virtual environment activated in your current PowerShell session, dot-source the script:

```powershell
. .\setup.ps1
```

The script prints colored status messages (yellow = action, cyan = notice, green = complete).

---

## 📋 Complete Endpoint Reference

### HTTP REST API Endpoints

| Method                        | Endpoint                                  | Description                                        | Auth Required |
| ----------------------------- | ----------------------------------------- | -------------------------------------------------- | ------------- |
| **General**                   |
| `GET`                         | `/`                                       | Serve main HTML page                               | No            |
| `GET`                         | `/api`                                    | API status check                                   | No            |
| `GET`                         | `/api/system/status`                      | System status & statistics                         | No            |
| **App Info CRUD**             |
| `GET`                         | `/api/app-info`                           | Get all app info records                           | No            |
| `GET`                         | `/api/app-info/{id}`                      | Get specific app info by ID                        | No            |
| `POST`                        | `/api/app-info`                           | Create new app info                                | No            |
| `PUT`                         | `/api/app-info/{id}`                      | Update app info by ID                              | No            |
| `DELETE`                      | `/api/app-info/{id}`                      | Delete app info by ID                              | No            |
| **Stress History CRUD**       |
| `GET`                         | `/api/stress-history`                     | Get all stress history records                     | No            |
| `GET`                         | `/api/stress-history/{id}`                | Get specific stress record                         | No            |
| `POST`                        | `/api/stress-history`                     | Create new stress record                           | No            |
| `PUT`                         | `/api/stress-history/{id}`                | Update stress record                               | No            |
| `DELETE`                      | `/api/stress-history/{id}`                | Delete stress record                               | No            |
| **Measurement Sessions CRUD** |
| `GET`                         | `/api/sessions`                           | Get all measurement sessions                       | No            |
| `GET`                         | `/api/sessions/{id}`                      | Get specific session by ID                         | No            |
| `POST`                        | `/api/sessions`                           | Create new measurement session                     | No            |
| `DELETE`                      | `/api/sessions/{id}`                      | Delete session by ID                               | No            |
| **Sensor Readings CRUD**      |
| `GET`                         | `/api/sensor-readings`                    | Get all sensor readings                            | No            |
| `GET`                         | `/api/sensor-readings/{id}`               | Get specific sensor reading                        | No            |
| `GET`                         | `/api/sessions/{id}/sensor-readings`      | Get sensor readings for a session                  | No            |
| `POST`                        | `/api/sensor-readings`                    | Create new sensor reading                          | No            |
| `POST`                        | `/api/sessions/{id}/sensor-readings/bulk` | Create multiple readings for a session             | No            |
| `PUT`                         | `/api/sensor-readings/{id}`               | Update sensor reading                              | No            |
| `DELETE`                      | `/api/sensor-readings/{id}`               | Delete sensor reading                              | No            |
| **ML Prediction**             |
| `POST`                        | `/api/predict-stress`                     | Predict stress from sensor data                    | No            |
| **ESP32 HTTP Fallback**       |
| `POST`                        | `/api/esp32/data`                         | HTTP fallback for ESP32 (if WebSocket unavailable) | No            |
| **WebSocket Info**            |
| `GET`                         | `/api/websocket/info`                     | Get WebSocket connection info & events             | No            |
| `GET`                         | `/api/websocket/test`                     | WebSocket test HTML page                           | No            |

### WebSocket Events (Real-time Relay)

**Connection URL:** `ws://127.0.0.1:5000/socket.io/?EIO=4&transport=websocket&type={client_type}`

| Event Name                | Direction         | Client Type    | Description                             | Payload                                               |
| ------------------------- | ----------------- | -------------- | --------------------------------------- | ----------------------------------------------------- |
| **Connection Management** |
| `connect`                 | Server → Client   | All            | Connection established                  | Auto-emits `connection_status`                        |
| `disconnect`              | Server → Client   | All            | Connection closed                       | Auto-updates `client_stats`                           |
| `connection_status`       | Server → Client   | ESP32/Frontend | Connection confirmation                 | `{status, message}`                                   |
| `client_stats`            | Server → Frontend | Frontend       | Active client counts                    | `{frontend_clients, esp32_clients, total_clients}`    |
| **ESP32 Data Stream**     |
| `esp32_live_data`         | ESP32 → Server    | ESP32          | Send sensor data (real-time relay only) | `{hr, temp, eda, timestamp?, device_id?}`             |
| `live_data_received`      | Server → ESP32    | ESP32          | Confirmation of data receipt            | `{status, message}`                                   |
| `live_sensor_data`        | Server → Frontend | Frontend       | Broadcast sensor data                   | `{timestamp, hr, temp, eda, device_id}`               |
| **Utility Events**        |
| `ping`                    | Client → Server   | All            | Connection health check                 | Send `2` (Engine.IO ping)                             |
| `pong`                    | Server → Client   | All            | Ping response                           | `{timestamp}`                                         |
| `health_check`            | Client → Server   | All            | Server health status                    | Empty or `{}`                                         |
| `health_status`           | Server → Client   | All            | Health response                         | `{status, timestamp, connected_clients, server_info}` |
| `error`                   | Server → Client   | All            | Error notification                      | `{message}`                                           |

### WebSocket Client Types

| Type       | Query Param      | Can Send                                  | Can Receive                                                              | Purpose                           |
| ---------- | ---------------- | ----------------------------------------- | ------------------------------------------------------------------------ | --------------------------------- |
| `esp32`    | `?type=esp32`    | `esp32_live_data`, `ping`, `health_check` | `live_data_received`, `connection_status`, `pong`, `error`               | ESP32 devices sending sensor data |
| `frontend` | `?type=frontend` | `ping`, `health_check`                    | `live_sensor_data`, `client_stats`, `connection_status`, `pong`, `error` | React/web clients receiving data  |

---

## 📊 Database Schema

The application uses the following database tables with relationships:

### Tables Overview

1. **`app_info`** - Application metadata
2. **`measurement_sessions`** - Groups related stress measurements (uses UUID)
3. **`stress_history`** - Stress prediction results linked to sessions
4. **`sensor_readings`** - Raw sensor data linked to sessions

### Table Relationships

```
measurement_sessions (1) ──< (many) stress_history
measurement_sessions (1) ──< (many) sensor_readings
```

### Table: `measurement_sessions`

Stores measurement session information. Each session represents a single stress prediction event.

| Column       | Type       | Description                               |
| ------------ | ---------- | ----------------------------------------- |
| `id`         | String(36) | Primary key (UUID, e.g., "a1b2c3d4-...")  |
| `created_at` | DateTime   | Session creation timestamp (Jakarta time) |
| `notes`      | Text       | Optional notes about the session          |

### Table: `stress_history`

Stores stress prediction results with reference to measurement sessions.

| Column             | Type       | Description                                      |
| ------------------ | ---------- | ------------------------------------------------ |
| `id`               | Integer    | Primary key (auto-increment)                     |
| `session_id`       | String(36) | Foreign key to `measurement_sessions.id`         |
| `timestamp`        | DateTime   | Prediction timestamp (Jakarta time)              |
| `hr`               | Float      | Heart rate (BPM)                                 |
| `temp`             | Float      | Temperature (°C)                                 |
| `eda`              | Float      | Electrodermal activity                           |
| `label`            | String     | Stress level ("Normal", "Medium", "High Stress") |
| `confidence_level` | Float      | Model confidence (0.0 - 1.0)                     |
| `notes`            | Text       | Additional notes                                 |
| `created_at`       | DateTime   | Record creation timestamp                        |

### Table: `sensor_readings`

Stores raw sensor readings linked to measurement sessions.

| Column       | Type       | Description                              |
| ------------ | ---------- | ---------------------------------------- |
| `id`         | Integer    | Primary key (auto-increment)             |
| `session_id` | String(36) | Foreign key to `measurement_sessions.id` |
| `timestamp`  | DateTime   | Reading timestamp (Jakarta time)         |
| `hr`         | Float      | Heart rate (BPM)                         |
| `temp`       | Float      | Temperature (°C)                         |
| `eda`        | Float      | Electrodermal activity                   |
| `created_at` | DateTime   | Record creation timestamp                |

### Stress Prediction Flow

When `/api/predict-stress` is called:

1. **Create Session** - A new `measurement_session` is created with UUID
2. **Predict Stress** - ML model processes sensor data
3. **Save Sensor Reading** - Raw sensor data saved to `sensor_readings` with session reference
4. **Save Prediction** - Prediction result saved to `stress_history` with session reference

Response includes `session_id`, `history_id`, and `sensor_reading_id` for tracking.

---

## API Documentation

The application provides RESTful API endpoints for managing app information.

### Base URL

When running locally: `http://127.0.0.1:5000`

### Endpoints

#### Get all app info records

```http
GET /api/app-info
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "app_name": "My App",
      "app_version": "1.0.0",
      "description": "Sample app",
      "owner": "Developer",
      "contact": "dev@example.com",
      "created_at": "2025-01-01T00:00:00",
      "updated_at": "2025-01-01T00:00:00"
    }
  ]
}
```

#### Get specific app info

```http
GET /api/app-info/{id}
```

Response: Same format as above but with single record in `data`.

#### Create new app info

```http
POST /api/app-info
Content-Type: application/json

{
  "app_name": "My New App",
  "app_version": "1.0.0",
  "description": "Description here",
  "owner": "Owner name",
  "contact": "contact@example.com"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "id": 2,
    "app_name": "My New App"
    // ... other fields
  }
}
```

#### Update app info

```http
PUT /api/app-info/{id}
Content-Type: application/json

{
  "app_name": "Updated App Name",
  "description": "Updated description"
}
```

Response: Same format as create.

#### Delete app info

```http
DELETE /api/app-info/{id}
```

Response:

```json
{
  "success": true,
  "message": "App info deleted successfully"
}
```

#### Stress history (stress_history)

APIs for storing and retrieving stress test readings (heart rate, temperature, EDA, labels, etc.).

Get all records

```http
GET /api/stress-history
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "timestamp": "2025-12-01T12:00:00",
      "hr": 72.5,
      "temp": 36.6,
      "eda": 0.12,
      "label": "normal",
      "confidence_level": 0.95,
      "notes": "sample",
      "created_at": "2025-12-01T12:00:01"
    }
  ]
}
```

Get specific record

```http
GET /api/stress-history/{id}
```

Create new record

```http
POST /api/stress-history
Content-Type: application/json

{
  "hr": 72.5,
  "temp": 36.6,
  "eda": 0.12,
  "label": "normal",
  "confidence_level": 0.95,
  "notes": "sample"  # optional; if omitted the server will store an empty string
}
```

Update record

```http
PUT /api/stress-history/{id}
Content-Type: application/json

{
  "hr": 75.0,
  "notes": "adjusted"
}
```

Delete record

```http
DELETE /api/stress-history/{id}
```

### curl examples for stress history

```powershell
# List all
curl http://127.0.0.1:5000/api/stress-history

# Create (do not include `timestamp`; server sets it)
curl -X POST http://127.0.0.1:5000/api/stress-history -H "Content-Type: application/json" -d '{"hr":72.5,"temp":36.6,"eda":0.12,"label":"normal"}'

# Get
curl http://127.0.0.1:5000/api/stress-history/1

# Update
curl -X PUT http://127.0.0.1:5000/api/stress-history/1 -H "Content-Type: application/json" -d '{"notes":"updated"}'

# Delete
curl -X DELETE http://127.0.0.1:5000/api/stress-history/1
```

### ML model prediction

Predict stress label using the included scaler and RandomForest classifier stored in `models/`.

**Important:** This endpoint automatically creates a measurement session and saves both sensor readings and prediction results to the database.

Endpoint:

```http
POST /api/predict-stress
Content-Type: application/json
```

Request body (JSON):

```json
{
  "hr": 70.0,
  "temp": 36.5,
  "eda": 5.0,
  "notes": "Optional session notes"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "hr": 70.0,
    "temp": 36.5,
    "eda": 5.0,
    "label": "Normal",
    "confidence_level": 0.54
  },
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "history_id": 1,
  "sensor_reading_id": 1
}
```

**Flow:**

1. Creates a new `measurement_session` (with UUID)
2. Performs ML prediction
3. Saves raw sensor data to `sensor_readings`
4. Saves prediction result to `stress_history`
5. Returns all IDs for tracking

Notes:

- The server loads `models/scaler_model.pkl` and `models/classification_rf_model.pkl` from the project `models/` folder.
- All timestamps are automatically set to Jakarta timezone (UTC+7).
- Requires `joblib` and `pandas` installed in the environment.

Curl example:

```powershell
curl -X POST http://127.0.0.1:5000/api/predict-stress -H "Content-Type: application/json" -d '{"hr":70,"temp":36.5,"eda":5,"notes":"Test prediction"}'
```

### Measurement Sessions API

Manage measurement sessions that group related stress measurements.

#### Get all sessions

```http
GET /api/sessions
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "created_at": "2025-12-11T14:30:00+07:00",
      "notes": "Stress prediction session"
    }
  ]
}
```

#### Get specific session

```http
GET /api/sessions/{session_id}
```

#### Create new session

```http
POST /api/sessions
Content-Type: application/json

{
  "notes": "Manual session creation"
}
```

Note: Session ID (UUID) and timestamp are auto-generated.

#### Delete session

```http
DELETE /api/sessions/{session_id}
```

**Warning:** Deleting a session may affect related `stress_history` and `sensor_readings` records.

### Sensor Readings API

Manage raw sensor readings linked to measurement sessions.

#### Get all sensor readings

```http
GET /api/sensor-readings
```

Response:

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "timestamp": "2025-12-11T14:30:00+07:00",
      "hr": 75.5,
      "temp": 36.6,
      "eda": 0.45,
      "created_at": "2025-12-11T14:30:01+07:00"
    }
  ]
}
```

#### Get sensor readings for a session

```http
GET /api/sessions/{session_id}/sensor-readings
```

Returns all sensor readings associated with a specific session, ordered by timestamp.

#### Get specific sensor reading

```http
GET /api/sensor-readings/{reading_id}
```

#### Create new sensor reading

```http
POST /api/sensor-readings
Content-Type: application/json

{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "hr": 75.5,
  "temp": 36.6,
  "eda": 0.45
}
```

All fields are required. Timestamp is auto-generated in Jakarta timezone.

#### Update sensor reading

```http
PUT /api/sensor-readings/{reading_id}
Content-Type: application/json

{
  "hr": 76.0,
  "temp": 36.7
}
```

#### Delete sensor reading

```http
DELETE /api/sensor-readings/{reading_id}
```

#### Bulk create sensor readings

Create multiple sensor readings for a session in one request.

```http
POST /api/sessions/{session_id}/sensor-readings/bulk
Content-Type: application/json

{
  "readings": [
    {"hr": 75.5, "temp": 36.6, "eda": 0.45},
    {"hr": 76.0, "temp": 36.7, "eda": 0.48},
    {"hr": 74.8, "temp": 36.5, "eda": 0.42}
  ]
}
```

**Request format:**

- `readings` (required): Array of sensor reading objects
- Each reading must have: `hr`, `temp`, `eda` (all required)
- `session_id` is taken from URL path
- Each reading gets its own auto-generated `timestamp`

**Response:**

```json
{
  "success": true,
  "created_count": 3,
  "error_count": 0,
  "data": [
    {
      "id": 1,
      "session_id": "a1b2c3d4-...",
      "timestamp": "2025-12-11T14:30:00+07:00",
      "hr": 75.5,
      "temp": 36.6,
      "eda": 0.45,
      "created_at": "2025-12-11T14:30:01+07:00"
    },
    {
      "id": 2,
      "session_id": "a1b2c3d4-...",
      "timestamp": "2025-12-11T14:30:02+07:00",
      "hr": 76.0,
      "temp": 36.7,
      "eda": 0.48,
      "created_at": "2025-12-11T14:30:03+07:00"
    },
    {
      "id": 3,
      "session_id": "a1b2c3d4-...",
      "timestamp": "2025-12-11T14:30:04+07:00",
      "hr": 74.8,
      "temp": 36.5,
      "eda": 0.42,
      "created_at": "2025-12-11T14:30:05+07:00"
    }
  ]
}
```

**Notes:**

- If some readings have errors, valid ones will still be saved
- Response includes `created_count` and `error_count`
- Any errors are listed in `errors` array with index and error message
- All timestamps use Jakarta timezone (UTC+7)

### Curl Examples for New Endpoints

```powershell
# Create a session
curl -X POST http://127.0.0.1:5000/api/sessions -H "Content-Type: application/json" -d '{"notes":"Test session"}'

# Get all sessions
curl http://127.0.0.1:5000/api/sessions

# Create sensor reading
curl -X POST http://127.0.0.1:5000/api/sensor-readings -H "Content-Type: application/json" -d '{"session_id":"YOUR-UUID-HERE","hr":75.5,"temp":36.6,"eda":0.45}'

# Bulk create sensor readings
curl -X POST http://127.0.0.1:5000/api/sessions/YOUR-UUID-HERE/sensor-readings/bulk -H "Content-Type: application/json" -d '{"readings":[{"hr":75.5,"temp":36.6,"eda":0.45},{"hr":76.0,"temp":36.7,"eda":0.48}]}'

# Get sensor readings for a session
curl http://127.0.0.1:5000/api/sessions/YOUR-UUID-HERE/sensor-readings
```

### Error Responses

All endpoints return error responses in this format:

```json
{
  "success": false,
  "error": "Error message here"
}
```

### Testing API with curl

```powershell
# Get all records
curl http://127.0.0.1:5000/api/app-info

# Create new record
curl -X POST http://127.0.0.1:5000/api/app-info -H "Content-Type: application/json" -d '{\"app_name\":\"Test App\",\"app_version\":\"1.0\"}'

# Get specific record
curl http://127.0.0.1:5000/api/app-info/1

# Update record
curl -X PUT http://127.0.0.1:5000/api/app-info/1 -H "Content-Type: application/json" -d '{\"description\":\"Updated desc\"}'

# Delete record
curl -X DELETE http://127.0.0.1:5000/api/app-info/1
```
