#!/bin/bash
set -e

# Wait for database if needed (optional, Railway handles this well)
# but for robust production, we just run migrations.

echo "--- Starting Vantier Backend Entrypoint ---"

# Run migrations
echo "Running alembic migrations..."
alembic upgrade head

# Start the application
echo "Starting Uvicorn server on port ${PORT:-8000}..."
exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'
