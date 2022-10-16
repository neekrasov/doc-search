from functools import lru_cache

from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from db.elastic import get_elastic
from db.redis import get_redis
from services.posts import PostService


@lru_cache()
def get_post_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PostService:
    return PostService(redis, elastic)
