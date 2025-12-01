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
