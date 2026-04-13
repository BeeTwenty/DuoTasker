#!/usr/bin/env bash
set -euo pipefail

echo "Starting DuoTasker migration dry run..."

if [ ! -f ".venv/bin/python" ]; then
  echo "Missing .venv Python. Create virtual environment first."
  exit 1
fi

.venv/bin/python manage.py check
.venv/bin/python manage.py test --settings=DuoTasker.test_settings
.venv/bin/python manage.py showmigrations
.venv/bin/python manage.py migrate --plan

echo "Dry run completed successfully."
