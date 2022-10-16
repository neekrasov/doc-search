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
    elastic.es = AsyncElasticsearch(
        hosts=[f"http://{settings.elastic_host}:{settings.elastic_port}"]
    )
    
    exists = await elastic.es.indices.exists(index="posts")
    
    if not exists:
        logging.info("Elasticsearch: Index 'posts' not ready")
    else:
        logging.info("Elasticsearch: Index 'posts' ready")
        
    assert await redis.redis.ping(), "Redis is not available"
    logging.info("Redis: Ready")


async def shutdown():
    await redis.redis.close()
    await elastic.es.close()
