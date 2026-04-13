#!/bin/sh
set -eu

wait_for_service() {
	host="$1"
	port="$2"
	name="$3"

	python - "$host" "$port" "$name" <<'PY'
import socket
import sys
import time

host, port, name = sys.argv[1], int(sys.argv[2]), sys.argv[3]
for _ in range(60):
	try:
		with socket.create_connection((host, port), timeout=2):
			print(f"{name} is available")
			sys.exit(0)
	except OSError:
		time.sleep(1)

print(f"Timed out waiting for {name} at {host}:{port}", file=sys.stderr)
sys.exit(1)
PY
}

echo "Waiting for PostgreSQL..."
wait_for_service "${DB_HOST:-postgres}" "${DB_PORT:-5432}" "PostgreSQL"

echo "Waiting for Redis..."
wait_for_service "${REDIS_HOST:-redis}" "${REDIS_PORT:-6379}" "Redis"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput


# Start server
echo "Starting server..."
exec uvicorn DuoTasker.asgi:application --host 0.0.0.0 --port 8000



