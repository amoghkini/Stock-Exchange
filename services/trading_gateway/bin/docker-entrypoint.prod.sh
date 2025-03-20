#!/bin/bash
set -e

echo "Starting the FastAPI application in production mode..."

cd /app/src

export PYTHONPATH="/path/to/dir1:$PYTHONPATH"

# Start the production server with Gunicorn and Uvicorn workers
exec gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 main:app
