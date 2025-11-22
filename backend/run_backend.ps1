# PowerShell script to start ElectroFix Django backend without chaining
# Usage: pwsh -File run_backend.ps1

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $root '..' '..' '.venv' 'Scripts' 'python.exe'
$managePy = Join-Path $root 'manage.py'

if (!(Test-Path $managePy)) {
    Write-Error "manage.py not found at $managePy"
}
if (!(Test-Path $venvPython)) {
    Write-Error "venv python not found at $venvPython"
}

Write-Host "Starting Django on http://127.0.0.1:8000 using $venvPython" -ForegroundColor Cyan
& $venvPython $managePy runserver 127.0.0.1:8000
