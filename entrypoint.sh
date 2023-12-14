#!/bin/bash

# Activate the virtual environment
. /app/venv/bin/activate

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser
echo "Creating superuser..."
python manage.py createinitialsuperuser


# Start server
echo "Starting server..."
uvicorn DuoTasker.asgi:application --host 0.0.0.0 --port 8000



