$venv = Join-Path $PSScriptRoot '.venv'
if (-Not (Test-Path $venv)) {
    python -m venv $venv
}
$activate = Join-Path $venv 'Scripts\Activate.ps1'
if (-Not (Test-Path $activate)) {
    Write-Error "Activation script not found: $activate"
    exit 1
}
. $activate
python -m pip install --upgrade pip
$req = Join-Path $PSScriptRoot 'requirements.txt'
if (Test-Path $req) {
    python -m pip install -r $req
}
