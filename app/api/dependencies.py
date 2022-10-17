from functools import cache
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from services.posts import PostService
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis


async def get_redis() -> Redis:
    raise NotImplementedError


async def get_elastic() -> AsyncElasticsearch:
    raise NotImplementedError


@cache
def get_post_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PostService:
    return PostService(redis, elastic)
