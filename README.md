# Flask Stress App (minimal scaffold)

Minimal Flask scaffold for local development.

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
    "app_name": "My New App",
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
