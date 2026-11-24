$ErrorActionPreference = "Stop"
Write-Host "=== Day 2 - PyAutoGUIBasic setup ===" -ForegroundColor Cyan

python --version
if ($LASTEXITCODE -ne 0) {
    throw "Python was not found. Install Python 3.12 and enable Add Python to PATH."
}

if (-not (Test-Path ".\venv")) {
    python -m venv venv
}

.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "Setup completed. Next run: python daily_report_bot.py" -ForegroundColor Green
