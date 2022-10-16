import json
from pprint import pprint
from schemas.posts import Post
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis
from core.settings import get_settings
from pydantic.json import pydantic_encoder
from pydantic import parse_raw_as

settings = get_settings()


class PostService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_posts(self, search_text: str) -> list[Post] | None:
        posts = await self._get_posts_from_cache(search_text)
        if not posts:
            posts = await self._get_posts_from_elastic(search_text)
        if not posts:
            return None
        await self._put_posts_to_cache(search_text, posts)
        return posts

    async def _get_posts_from_elastic(self, search_text: str) -> list[Post] | None:
        posts = await self.elastic.search(
            index="posts",
            query={"match": {"text": search_text}},
            sort="created_date:desc",
            size=10,
        )
        return [
            Post(id=post["_id"], **post["_source"])
            for post in posts.body["hits"]["hits"]
        ]

    async def _get_posts_from_cache(self, search_text: str) -> list[Post] | None:
        data = await self.redis.get(search_text)
        if not data:
            return None
        posts = parse_raw_as(list[Post], data)
        return posts

    async def _put_posts_to_cache(self, search_text: str, posts: list[Post]):
        await self.redis.set(
            name=search_text,
            value=json.dumps(posts, default=pydantic_encoder),
            ex=settings.post_cache_expire_in_seconds,
        )
