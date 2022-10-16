import redis.asyncio as aredis
from elasticsearch import AsyncElasticsearch

from . import redis, elastic
from core.settings import get_settings
import logging

settings = get_settings()


async def startup():
    redis.redis = aredis.from_url(
        url=f"redis://{settings.redis_host}:{settings.redis_port}"
    )
    assert await redis.redis.ping(), "Redis is not available"
    logging.info("Redis: connection established")

    elastic.es = AsyncElasticsearch(
        hosts=[f"http://{settings.elastic_host}:{settings.elastic_port}"]
    )
    assert await elastic.es.ping()
    logging.info("Elasticsearch: connection established")

    assert await elastic.es.indices.exists(index="posts"), "Posts index does not exist"
    logging.info("Elasticsearch: Index 'posts' ready")


async def shutdown():
    await redis.redis.close()
    await elastic.es.close()
