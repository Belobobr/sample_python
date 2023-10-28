from fastapi import APIRouter, HTTPException
from config import Config
from typing import Callable

def create_health_router(config: Config) -> APIRouter:
    def health_live():
        return {"status": 'ok'}

    async def health_ready():
        return {"status": 'ok'}

    async def health_startup():
        return {"status": 'ok'}

    router = APIRouter()
    router.get("/health/live")(health_live)
    router.get("/health/ready")(health_ready)
    router.get("/health/startup")(health_startup)
    return router


