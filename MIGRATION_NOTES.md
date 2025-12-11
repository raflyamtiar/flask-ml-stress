# Database Migration Summary - Version 2.1.1

## Overview

Menambahkan sistem session-based tracking untuk pengukuran stress dengan UUID-based sessions.

## Perubahan Database

### Tabel Baru

1. **`measurement_sessions`**

   - Primary Key: `id` (String UUID, bukan auto-increment)
   - Fields: `created_at`, `notes`
   - Purpose: Mengelompokkan measurements yang terkait dalam satu sesi prediksi

2. **`sensor_readings`**
   - Primary Key: `id` (Integer auto-increment)
   - Foreign Key: `session_id` → `measurement_sessions.id`
   - Fields: `timestamp`, `hr`, `temp`, `eda`, `created_at`
   - Purpose: Menyimpan raw sensor data untuk setiap sesi

### Tabel yang Dimodifikasi

1. **`stress_history`**
   - Tambah kolom: `session_id` (Foreign Key ke `measurement_sessions.id`)
   - Purpose: Linking stress prediction results dengan session

## Alur Baru di `/api/predict-stress`

### Flow Lama:

1. Terima data sensor
2. Prediksi stress
3. Simpan ke `stress_history`

### Flow Baru:

1. **Buat session** → `measurement_sessions` (UUID auto-generated)
2. **Prediksi stress** → ML model processing
3. **Simpan sensor reading** → `sensor_readings` (linked to session)
4. **Simpan prediction** → `stress_history` (linked to session)
5. **Return** session_id, history_id, sensor_reading_id

## Endpoint Baru

### Measurement Sessions

- `GET /api/sessions` - List all sessions
- `GET /api/sessions/{id}` - Get specific session
- `POST /api/sessions` - Create new session
- `DELETE /api/sessions/{id}` - Delete session

### Sensor Readings

- `GET /api/sensor-readings` - List all readings
- `GET /api/sensor-readings/{id}` - Get specific reading
- `GET /api/sessions/{id}/sensor-readings` - Get readings by session
- `POST /api/sensor-readings` - Create new reading
- `POST /api/sessions/{id}/sensor-readings/bulk` - **[NEW]** Create multiple readings for a session
- `PUT /api/sensor-readings/{id}` - Update reading
- `DELETE /api/sensor-readings/{id}` - Delete reading

## Services Baru

1. **MeasurementSessionService**
   - create(), get_all(), get_by_id(), delete()
2. **SensorReadingService**
   - create(), get_all(), get_by_id(), get_by_session()
   - update(), delete()

## Timezone

Semua timestamp menggunakan Jakarta timezone (UTC+7):

- `created_at` di semua tabel
- `timestamp` di sensor_readings dan stress_history

## Migration Steps

1. Jalankan migration:

   ```powershell
   flask db upgrade
   ```

2. Atau recreate database:
   ```powershell
   # Backup dulu jika perlu
   # Kemudian jalankan
   python -c "from app import create_app; from app.models import create_tables; app = create_app(); create_tables(app)"
   ```

## Testing

Test endpoint predict-stress baru:

```powershell
curl -X POST http://127.0.0.1:5000/api/predict-stress `
  -H "Content-Type: application/json" `
  -d '{"hr":75.5,"temp":36.6,"eda":0.45,"notes":"Test session"}'
```

Expected response:

```json
{
  "success": true,
  "data": {
    "hr": 75.5,
    "temp": 36.6,
    "eda": 0.45,
    "label": "Normal",
    "confidence_level": 0.85
  },
  "session_id": "a1b2c3d4-...",
  "history_id": 1,
  "sensor_reading_id": 1
}
```

### Test Bulk Insert Sensor Readings

Kirim banyak sensor readings sekaligus untuk satu session:

```powershell
curl -X POST http://127.0.0.1:5000/api/sessions/YOUR-SESSION-UUID/sensor-readings/bulk `
  -H "Content-Type: application/json" `
  -d '{
    "readings": [
      {"hr":75.5,"temp":36.6,"eda":0.45},
      {"hr":76.0,"temp":36.7,"eda":0.48},
      {"hr":74.8,"temp":36.5,"eda":0.42}
    ]
  }'
```

Expected response:

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

**Catatan Bulk Insert:**

- Semua readings akan menggunakan `session_id` yang sama (dari URL)
- Setiap reading harus memiliki `hr`, `temp`, dan `eda`
- `timestamp` otomatis di-generate untuk setiap reading
- Jika ada error di beberapa readings, yang valid tetap akan tersimpan
- Response include `created_count` dan `error_count`

## Files Modified

1. `app/models.py` - Added MeasurementSession, SensorReading, updated HistoryStress
2. `app/service.py` - Added MeasurementSessionService, SensorReadingService
3. `app/routes.py` - Updated predict-stress endpoint, added CRUD endpoints
4. `README.md` - Updated documentation with new schema and endpoints
5. `migrations/versions/add_sessions_and_readings.py` - Migration script

## Breaking Changes

⚠️ Response dari `/api/predict-stress` sekarang include additional fields:

- `session_id` (UUID string)
- `sensor_reading_id` (integer)

Existing clients might need to handle these new fields.
