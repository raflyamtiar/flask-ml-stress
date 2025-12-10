# 🚀 Cara Menjalankan dan Test WebSocket Server

## 1️⃣ Menjalankan Server

### Langkah 1: Aktivasi Virtual Environment

```powershell
# Di folder project
.\.venv\Scripts\Activate.ps1
```

### Langkah 2: Jalankan Flask Server

```powershell
python run.py
```

Server akan berjalan di: `http://127.0.0.1:5000`

Output yang muncul:

```
WARNING:werkzeug: * Debugger is active!
INFO:werkzeug: * Debugger PIN: xxx-xxx-xxx
(xxxx) wsgi starting up on http://127.0.0.1:5000
```

---

## 2️⃣ Testing WebSocket

### A. Test di Browser (Paling Mudah)

1. Buka browser dan akses: **`http://127.0.0.1:5000/api/websocket/test`**
2. Klik tombol **"Connect as Frontend"**
3. Lihat connection log
4. Test fitur:
   - **Simulate ESP32**: Kirim data sensor simulasi
   - **Request History**: Minta data historis
   - **Auto Send**: Kirim data otomatis setiap 5 detik

---

### B. Test dengan Postman

#### ⚠️ **Penting**: Postman WebSocket Support

- Postman versi terbaru (2023+) sudah support WebSocket
- Atau gunakan extension: **Postman WebSocket Request**

#### Langkah Testing di Postman:

**1. Test HTTP Endpoints (REST API)**

Buat New Request → Type: **POST**

**Endpoint ESP32 HTTP Fallback:**

```
POST http://127.0.0.1:5000/api/esp32/data
```

**Headers:**

```
Content-Type: application/json
```

**Body (JSON):**

```json
{
  "hr": 75.5,
  "temp": 36.2,
  "eda": 0.45,
  "device_id": "ESP32_TEST",
  "timestamp": "2024-12-10T10:30:00Z"
}
```

**Expected Response:**

```json
{
  "success": true,
  "message": "Data received and processed successfully",
  "data": {
    "record_id": 1,
    "timestamp": "2024-12-10T10:30:00+00:00",
    "stress_prediction": {
      "label": "normal",
      "confidence": 85.5
    },
    "sensor_data": {
      "hr": 75.5,
      "temp": 36.2,
      "eda": 0.45
    }
  }
}
```

**2. Test WebSocket di Postman**

- Buka Postman
- Klik **New** → **WebSocket Request**
- Masukkan URL: `ws://127.0.0.1:5000/socket.io/?type=esp32&transport=websocket`

⚠️ **Catatan**: Socket.IO memerlukan handshake khusus, lebih mudah test dengan tools lain.

---

### C. Test dengan Python Script

Buat file `test_websocket.py`:

```python
import socketio
import time

# Create Socket.IO client
sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('✓ Connected to server')

@sio.on('disconnect')
def on_disconnect():
    print('✗ Disconnected from server')

@sio.on('data_received')
def on_data_received(data):
    print(f'✓ Server response: {data}')

@sio.on('error')
def on_error(error):
    print(f'✗ Error: {error}')

# Connect as ESP32
try:
    sio.connect('http://127.0.0.1:5000',
                transports=['websocket'],
                auth={'type': 'esp32'},
                wait_timeout=10)

    # Send sensor data
    sensor_data = {
        'hr': 75.5,
        'temp': 36.2,
        'eda': 0.45,
        'device_id': 'ESP32_PYTHON_TEST'
    }

    print(f'📤 Sending data: {sensor_data}')
    sio.emit('esp32_sensor_data', sensor_data)

    # Wait for response
    time.sleep(2)

    sio.disconnect()

except Exception as e:
    print(f'Error: {e}')
```

Jalankan:

```powershell
python test_websocket.py
```

---

### D. Test dengan cURL (HTTP Fallback)

```powershell
# Test endpoint info
curl http://127.0.0.1:5000/api/websocket/info

# Test system status
curl http://127.0.0.1:5000/api/system/status

# Send sensor data via HTTP
curl -X POST http://127.0.0.1:5000/api/esp32/data `
  -H "Content-Type: application/json" `
  -d '{\"hr\":75.5,\"temp\":36.2,\"eda\":0.45,\"device_id\":\"ESP32_CURL\"}'
```

Atau dengan PowerShell:

```powershell
$body = @{
    hr = 75.5
    temp = 36.2
    eda = 0.45
    device_id = "ESP32_PS"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/esp32/data" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

---

### E. Test dengan JavaScript Console (Browser)

Buka browser console (F12) di halaman test:

```javascript
// Connect sebagai frontend
const socket = io("http://127.0.0.1:5000", {
  query: { type: "frontend" },
});

socket.on("connect", () => {
  console.log("✓ Connected");
});

socket.on("new_sensor_data", (data) => {
  console.log("📡 New data:", data);
});

socket.on("stress_alert", (alert) => {
  console.log("🚨 Alert:", alert);
});

// Request history
socket.emit("frontend_request_history", { limit: 10 });

socket.on("history_data", (data) => {
  console.log("📚 History:", data);
});
```

---

## 3️⃣ Monitoring & Debugging

### Check Logs di Terminal

Server akan menampilkan log seperti:

```
INFO:app.events:Client connected: xyz123 (type: esp32)
INFO:app.events:Saved sensor data from ESP32_001: HR=75.5, Temp=36.2, EDA=0.45
```

### Check Database

```powershell
python
>>> from app import create_app, db
>>> from app.models import HistoryStress
>>> app = create_app()
>>> with app.app_context():
...     records = HistoryStress.query.all()
...     for r in records:
...         print(f"ID: {r.id}, HR: {r.hr}, Stress: {r.label}")
```

---

## 4️⃣ Testing Checklist

- [ ] Server berjalan tanpa error
- [ ] Bisa akses `http://127.0.0.1:5000/api/websocket/test`
- [ ] WebSocket connection berhasil di browser test page
- [ ] Simulate ESP32 berhasil kirim data
- [ ] Data tersimpan di database
- [ ] Frontend menerima real-time updates
- [ ] HTTP fallback endpoint bekerja
- [ ] Stress alert muncul untuk high stress

---

## 5️⃣ Troubleshooting

### Error: "Address already in use"

```powershell
# Cari proses yang pakai port 5000
netstat -ano | findstr :5000

# Kill proses (ganti PID dengan nomor dari perintah di atas)
taskkill /PID <PID> /F
```

### Error: "ModuleNotFoundError"

```powershell
# Pastikan venv aktif
.\.venv\Scripts\Activate.ps1

# Install ulang dependencies
pip install -r requirements.txt
```

### WebSocket tidak connect

- Pastikan server running
- Check firewall Windows
- Pastikan URL benar: `ws://127.0.0.1:5000/socket.io/`
- Lihat console browser untuk error messages

---

## 📌 Quick Reference

**Start Server:**

```powershell
.\.venv\Scripts\Activate.ps1
python run.py
```

**Test Browser:**

```
http://127.0.0.1:5000/api/websocket/test
```

**HTTP Test:**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/system/status"
```

**Stop Server:**

```
Ctrl + C
```
