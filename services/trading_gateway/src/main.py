from fastapi import FastAPI

from src.api.api import api_router


VERSION = "0.1"
app = FastAPI(
    title="Stock Exchange",
    description="A stock exchange API",
    version=VERSION,
    docs_url=f"/api/{VERSION}/docs",
    redoc_url=f"/api/{VERSION}/redoc",
)

app.include_router(api_router)
