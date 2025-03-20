#!/bin/bash
set -e

echo "Starting the FastAPI application in development mode..."

# Run database migrations or other setup tasks here

# Start the dev server with Uvicorn directly
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
