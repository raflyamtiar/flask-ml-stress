$venv = Join-Path $PSScriptRoot '.venv'
if (-Not (Test-Path $venv)) {
    Write-Host "[ACTION] creating venv" -ForegroundColor Yellow
    python -m venv $venv
} else {
    Write-Host "[INFO] venv already exists - skipping creation" -ForegroundColor Cyan
}
$activate = Join-Path $venv 'Scripts\Activate.ps1'
if (-Not (Test-Path $activate)) {
    Write-Error "Activation script not found: $activate"
    exit 1
}
. $activate
Write-Host "[ACTION] activating venv" -ForegroundColor Yellow
Write-Host "[ACTION] upgrading pip" -ForegroundColor Yellow
python -m pip install --upgrade pip
$req = Join-Path $PSScriptRoot 'requirements.txt'
if (Test-Path $req) {
    Write-Host "[PACKAGES] installing requirements from requirements.txt" -ForegroundColor Yellow
    python -m pip install -r $req
} else {
    Write-Host "[WARN] requirements.txt not found - skipping install" -ForegroundColor Cyan
}

# Ensure instance directory and sqlite DB exist
$instanceDir = Join-Path $PSScriptRoot 'instance'
if (-Not (Test-Path $instanceDir)) {
    Write-Host "[ACTION] creating instance directory" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $instanceDir | Out-Null
}
$dbFile = Join-Path $instanceDir 'database.sqlite'
if (-Not (Test-Path $dbFile)) {
    Write-Host "[ACTION] creating sqlite database at $dbFile" -ForegroundColor Yellow
    New-Item -ItemType File -Path $dbFile | Out-Null
} else {
    Write-Host "[INFO] instance database already exists - $dbFile" -ForegroundColor Cyan
}

Write-Host "[OK] complete" -ForegroundColor Green
