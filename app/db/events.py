import redis.asyncio as aredis
from elasticsearch import AsyncElasticsearch

from . import redis, elastic
from core.settings import get_settings

settings = get_settings()


async def startup():
    redis.redis = aredis.from_url(
        url=f"redis://{settings.redis_host}:{settings.redis_port}"
    )
    elastic.es = AsyncElasticsearch(
        hosts=[f"http://{settings.elastic_host}:{settings.elastic_port}"]
    )


async def shutdown():
    await redis.redis.close()
    await elastic.es.close()
