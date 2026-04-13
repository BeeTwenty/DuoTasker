$ErrorActionPreference = "Stop"

Write-Host "Starting DuoTasker migration dry run..."

if (-Not (Test-Path ".venv\Scripts\python.exe")) {
    throw "Missing .venv Python. Create virtual environment first."
}

.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test --settings=DuoTasker.test_settings
.\.venv\Scripts\python.exe manage.py showmigrations
.\.venv\Scripts\python.exe manage.py migrate --plan

Write-Host "Dry run completed successfully."
