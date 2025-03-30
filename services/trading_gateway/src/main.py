import os
import asyncio
from fastapi import FastAPI

from api.api import api_router
from startup_tasks import heartbeat_task
from exchange_manager.service_discovery.eureka_client import EurekaClient


APP_NAME: str = "Trading Gateway"
VERSION = "0.1"

app = FastAPI(
    title=APP_NAME,
    description="A stock exchange API",
    version=VERSION,
    docs_url=f"/api/{VERSION}/docs",
    redoc_url=f"/api/{VERSION}/redoc",
)

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    """Register service with Eureka and start heartbeat task."""
    eureka_url = os.environ.get("EUREKA_URL", "http://eureka:8761/eureka/")
    instance_port = 8000
    eureka_client = EurekaClient(APP_NAME, eureka_url, instance_port)

    # Store Eureka client in app state
    app.state.eureka_client = eureka_client  

    # Register service in a background thread
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, eureka_client.register)

    # Start background heartbeat task
    asyncio.create_task(heartbeat_task(eureka_client))

@app.on_event("shutdown")
async def shutdown_event():
    """Deregister service from Eureka on shutdown."""
    eureka_client = app.state.eureka_client  # Retrieve Eureka client from app state
    if eureka_client:
        eureka_client.deregister()
