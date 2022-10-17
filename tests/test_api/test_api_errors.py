from elasticsearch import AsyncElasticsearch
from httpx import AsyncClient
import pytest
from redis.asyncio import Redis


@pytest.mark.asyncio
async def test_search_posts_error(client: AsyncClient, redis: Redis):
    response = await client.post("/api/v1/search", json={"text": "testtt"})
    redis_response = await redis.get("testtt")

    assert response.status_code == 404
    assert redis_response is None
    assert response.json() == {"detail": "Posts not found"}


@pytest.mark.asyncio
async def test_delete_post_error(client: AsyncClient, es: AsyncElasticsearch):
    response = await client.delete(f"/api/v1/delete/123")

    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}


@pytest.mark.asyncio
async def test_get_post_error(client: AsyncClient, es: AsyncElasticsearch):
    response = await client.get(f"/api/v1/post/123")

    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}
