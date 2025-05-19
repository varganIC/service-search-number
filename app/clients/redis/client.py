from typing import Optional

import redis.asyncio as redis

from app.config import settings


class Redis:
    def __init__(self):
        self.client: Optional[redis.Redis] = None

    def connect(self) -> None:
        self.client: redis.Redis = redis.Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            db=settings.redis.db,
            decode_responses=True
        )

    async def close(self) -> None:
        await self.client.close()


redis_instance = Redis()


def start_redis_client() -> None:
    redis_instance.connect()


async def stop_redis_client() -> None:
    await redis_instance.close()


def get_redis_instance() -> Redis:
    return redis_instance
