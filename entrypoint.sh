#!/bin/bash
set -e

PORT=${PORT:-8002}

echo "Running database migrations..."
alembic upgrade head

echo "Starting BHIV MDU Registry API..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"