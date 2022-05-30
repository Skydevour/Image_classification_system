import aioredis
import asyncio
from utils import config

_redis = None


async def get_redis():
    global _redis
    if _redis is not None:
        return _redis
    _redis = await aioredis.create_redis_pool(
        'redis://' + config.REDIS_IP + ':' + str(config.REDIS_PORT),
        minsize=1,
        maxsize=5,
        loop=asyncio.get_event_loop())
    return _redis
