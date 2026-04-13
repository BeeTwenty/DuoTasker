# Development Workflow

## Setup

Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install ruff black isort mypy pytest pytest-django pre-commit daphne
```

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install ruff black isort mypy pytest pytest-django pre-commit daphne
```

## Daily Quality Loop

Windows PowerShell:
```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m mypy .
.\.venv\Scripts\python.exe -m pre_commit run --all-files
.\.venv\Scripts\python.exe manage.py test --settings=DuoTasker.test_settings
```

Linux/macOS:
```bash
ruff check .
ruff format --check .
mypy .
pre-commit run --all-files
python manage.py test --settings=DuoTasker.test_settings
```

## Run App

Legacy settings path:
```bash
python manage.py runserver
```

V2 settings path:
```bash
python manage_v2.py runserver
```

## Segment Completion Gate

A segment is complete only when:
- Django checks pass.
- All tests pass.
- No diagnostics are reported in changed files.
- REMAKE_SEGMENTS_STATUS.md is updated.
