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

| Method                  | Endpoint                   | Description                                        | Auth Required |
| ----------------------- | -------------------------- | -------------------------------------------------- | ------------- |
| **General**             |
| `GET`                   | `/`                        | Serve main HTML page                               | No            |
| `GET`                   | `/api`                     | API status check                                   | No            |
| `GET`                   | `/api/system/status`       | System status & statistics                         | No            |
| **App Info CRUD**       |
| `GET`                   | `/api/app-info`            | Get all app info records                           | No            |
| `GET`                   | `/api/app-info/{id}`       | Get specific app info by ID                        | No            |
| `POST`                  | `/api/app-info`            | Create new app info                                | No            |
| `PUT`                   | `/api/app-info/{id}`       | Update app info by ID                              | No            |
| `DELETE`                | `/api/app-info/{id}`       | Delete app info by ID                              | No            |
| **Stress History CRUD** |
| `GET`                   | `/api/stress-history`      | Get all stress history records                     | No            |
| `GET`                   | `/api/stress-history/{id}` | Get specific stress record                         | No            |
| `POST`                  | `/api/stress-history`      | Create new stress record                           | No            |
| `PUT`                   | `/api/stress-history/{id}` | Update stress record                               | No            |
| `DELETE`                | `/api/stress-history/{id}` | Delete stress record                               | No            |
| **ML Prediction**       |
| `POST`                  | `/api/predict-stress`      | Predict stress from sensor data                    | No            |
| **ESP32 HTTP Fallback** |
| `POST`                  | `/api/esp32/data`          | HTTP fallback for ESP32 (if WebSocket unavailable) | No            |
| **WebSocket Info**      |
| `GET`                   | `/api/websocket/info`      | Get WebSocket connection info & events             | No            |
| `GET`                   | `/api/websocket/test`      | WebSocket test HTML page                           | No            |

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
  "eda": 5.0
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
    "label": "No Stress",
    "confidence_level": 0.54
  }
}
```

Notes:

- The server loads `models/scaler_model.pkl` and `models/classification_rf_model.pkl` from the project `models/` folder.
- The request should only include `hr`, `temp`, and `eda` as numbers. The server sets the record timestamp when storing to DB (if used).
- Requires `joblib` and `pandas` installed in the environment.

Curl example:

```powershell
curl -X POST http://127.0.0.1:5000/api/predict-stress -H "Content-Type: application/json" -d '{"hr":70,"temp":36.5,"eda":5}'
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
