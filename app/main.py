import uvicorn
from fastapi import FastAPI

from app.api import metadata as meta
from app.api import number
from app.clients.redis.client import start_redis_client, stop_redis_client
from app.config import settings

app = FastAPI(title=meta.title)
app.include_router(number.router)


@app.on_event("startup")
async def startup_event():
    start_redis_client()


@app.on_event("shutdown")
async def shutdown_event():
    await stop_redis_client()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.app.host,
        port=settings.app.port
    )
