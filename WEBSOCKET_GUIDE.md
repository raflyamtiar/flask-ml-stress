# WebSocket Server Implementation - Documentation

## 🎯 Overview

Successfully implemented a WebSocket server using Flask-SocketIO for real-time stress monitoring with ESP32 sensor integration and React frontend support.

## ✅ Features Implemented

### 1. **WebSocket Server with Flask-SocketIO**

- Real-time bidirectional communication
- Eventlet-based async support
- CORS enabled for cross-origin requests
- Connection management with client type tracking

### 2. **ESP32 Integration**

- **WebSocket Endpoint**: `esp32_sensor_data`
- **HTTP Fallback**: `POST /api/esp32/data`
- Accepts: HR (heart rate), Temperature, EDA (electrodermal activity)
- Automatic stress level prediction using ML models
- Real-time data validation and storage

### 3. **React Frontend Support**

- **WebSocket Events**: `new_sensor_data`, `stress_alert`, `client_stats`
- **Control Events**: `frontend_request_history`, `ping`, `health_check`
- Real-time stress alerts for high stress levels
- Historical data on-demand

### 4. **Database Integration**

- Automatic storage to `HistoryStress` model
- Timestamp handling (Unix/ISO formats)
- Confidence level tracking
- Device identification support

## 🌐 API Endpoints

### WebSocket Connection

```
ws://127.0.0.1:5000/socket.io/
```

#### Connection Parameters:

- ESP32: `?type=esp32`
- Frontend: `?type=frontend`

### HTTP Endpoints

- **WebSocket Info**: `GET http://127.0.0.1:5000/api/websocket/info`
- **System Status**: `GET http://127.0.0.1:5000/api/system/status`
- **Test Page**: `GET http://127.0.0.1:5000/api/websocket/test`
- **ESP32 HTTP Fallback**: `POST http://127.0.0.1:5000/api/esp32/data`

## 📡 WebSocket Events

### ESP32 → Server

```json
// Event: esp32_sensor_data
{
  "hr": 75.5,
  "temp": 36.2,
  "eda": 0.45,
  "timestamp": "2024-12-10T10:30:00Z", // optional
  "device_id": "ESP32_001" // optional
}
```

### Server → ESP32

```json
// Event: data_received
{
  "status": "success",
  "record_id": 123,
  "stress_prediction": {
    "label": "normal",
    "confidence": 0.85
  }
}
```

### Server → Frontend

```json
// Event: new_sensor_data
{
  "id": 123,
  "timestamp": "2024-12-10T10:30:00Z",
  "hr": 75.5,
  "temp": 36.2,
  "eda": 0.45,
  "stress_level": "normal",
  "confidence": 85.0,
  "device_id": "ESP32_001"
}

// Event: stress_alert (high stress detected)
{
  "type": "stress_alert",
  "level": "high_stress",
  "confidence": 87.5,
  "message": "High stress level detected...",
  "sensor_data": { "hr": 95, "temp": 37.1, "eda": 0.8 }
}
```

### Frontend → Server

```json
// Request historical data
// Event: frontend_request_history
{
  "limit": 100,
  "start_date": "2024-12-01", // optional
  "end_date": "2024-12-10"    // optional
}

// Subscribe to alerts
// Event: frontend_subscribe_alerts
{}

// Health check
// Event: ping
{}
```

## 🚀 Getting Started

### 1. Start the Server

```powershell
# In project directory
.venv\Scripts\Activate.ps1
python run.py
```

### 2. Test WebSocket

Open browser: `http://127.0.0.1:5000/api/websocket/test`

### 3. ESP32 Code Example

```cpp
#include <WiFi.h>
#include <SocketIOclient.h>

SocketIOclient socketIO;

void setup() {
  // WiFi setup...
  socketIO.begin("127.0.0.1", 5000, "/socket.io/?type=esp32");
  socketIO.onEvent(socketIOEvent);
}

void sendSensorData() {
  String payload = String("{\"hr\":") + getHeartRate() +
                   ",\"temp\":" + getTemperature() +
                   ",\"eda\":" + getEDA() +
                   ",\"device_id\":\"ESP32_001\"}";
  socketIO.sendEVENT("esp32_sensor_data", payload);
}
```

### 4. React Frontend Example

```javascript
import io from "socket.io-client";

const socket = io("ws://127.0.0.1:5000", {
  query: { type: "frontend" },
});

// Listen for real-time data
socket.on("new_sensor_data", (data) => {
  console.log("New sensor data:", data);
  updateUI(data);
});

// Listen for stress alerts
socket.on("stress_alert", (alert) => {
  showAlert(`Stress Alert: ${alert.level} (${alert.confidence}%)`);
});

// Request historical data
socket.emit("frontend_request_history", { limit: 50 });
socket.on("history_data", (data) => {
  console.log("History:", data.data);
});
```

## 📊 Data Flow

1. **ESP32** → Sends sensor data via WebSocket
2. **Server** → Validates data & runs ML prediction
3. **Database** → Stores sensor data + prediction results
4. **Frontend** → Receives real-time updates
5. **Alerts** → Automatic stress alerts for high confidence predictions

## 🔧 Configuration

### Environment Variables (.env)

```
SECRET_KEY=your-secret-key
FLASK_APP=run.py
FLASK_ENV=development
```

### Dependencies (requirements.txt)

- Flask-SocketIO==5.5.1
- eventlet==0.40.4
- Flask-CORS==6.0.1
- All other ML and database dependencies included

## 🧪 Testing

The implementation includes:

- ✅ WebSocket test page with ESP32 simulator
- ✅ Real-time connection monitoring
- ✅ Stress alert testing
- ✅ Historical data requests
- ✅ Auto-send functionality for continuous testing
- ✅ Connection statistics tracking

## 📝 Notes

- **Connection Types**: Server distinguishes between ESP32 and frontend clients
- **Error Handling**: Comprehensive error handling with detailed logging
- **Scalability**: Supports multiple ESP32 devices and frontend clients
- **Fallback**: HTTP endpoints available if WebSocket unavailable
- **Security**: CORS configured, input validation implemented
- **Monitoring**: Real-time client statistics and health checks

The server is now ready for production use with both ESP32 devices and React frontend applications!
