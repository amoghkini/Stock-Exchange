#!/bin/bash
set -e

echo "Starting the FastAPI application in production mode..."

# Run database migrations or other setup tasks here

# Start the production server with Gunicorn and Uvicorn workers
exec gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 src.main:app
