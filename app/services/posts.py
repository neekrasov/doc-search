import json

import elasticsearch
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

    async def search_posts(self, search_text: str) -> list[Post] | None:
        posts = await self._get_posts_from_cache(search_text)
        if not posts:
            posts = await self._search_posts_in_elastic(search_text)
        if not posts:
            return None
        await self._put_posts_to_cache(search_text, posts)
        return posts

    async def delete_post(self, post_id: str):
        try:
            await self.elastic.delete(index="posts", id=post_id)
        except elasticsearch.NotFoundError:
            return False

    async def get_post_by_id(self, post_id: str) -> Post | None:
        post = await self._get_post_from_cache(post_id)
        if not post:
            post = await self._get_post_in_elastic(post_id)
        if not post:
            return None
        await self._put_post_to_cache(post)
        return post

    async def _search_posts_in_elastic(self, search_text: str) -> list[Post] | None:
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

    async def _get_post_in_elastic(self, post_id: str) -> Post | None:
        try:
            post = await self.elastic.get(index="posts", id=post_id)
        except elasticsearch.NotFoundError:
            return None
        return Post(id=post_id, **post["_source"])

    async def _get_posts_from_cache(self, search_text: str) -> list[Post] | None:
        data = await self.redis.get(search_text)
        if not data:
            return None
        posts = parse_raw_as(list[Post], data)
        return posts

    async def _get_post_from_cache(self, post_id: str) -> Post | None:
        data = await self.redis.get(post_id)
        if not data:
            return None
        post = Post.parse_raw(data)
        return post

    async def _put_posts_to_cache(self, search_text: str, posts: list[Post]):
        await self.redis.set(
            name=search_text,
            value=json.dumps(posts, default=pydantic_encoder),
            ex=settings.post_cache_expire_in_seconds,
        )

    async def _put_post_to_cache(self, post: Post):
        await self.redis.set(
            name=post.id,
            value=json.dumps(post, default=pydantic_encoder),
            ex=settings.post_cache_expire_in_seconds,
        )
