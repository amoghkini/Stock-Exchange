#!/bin/bash
set -e

echo "Starting the FastAPI application in development mode..."

cd /app/src

# Start the dev server with Uvicorn directly
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
