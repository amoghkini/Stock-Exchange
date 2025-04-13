import logging
import asyncio

from fastapi import FastAPI
from exchange_manager.service_discovery.eureka_client import EurekaClient


HEARTBEAT_TIME_IN_SEC: int = 30

        
async def register_eureka(
    app: FastAPI,
    eureka_client: EurekaClient
) -> None:
    if eureka_client.register():
        asyncio.create_task(heartbeat_task(eureka_client))
    else:
        logging.error("Failed to register with Eureka")
    

async def heartbeat_task(eureka_client: EurekaClient) -> None:
    """Sends heartbeats to Eureka periodically."""
    while True:
        if not eureka_client.send_heartbeat():
            print("Heartbeat failed! Service might get deregistered.")
        await asyncio.sleep(HEARTBEAT_TIME_IN_SEC)
        