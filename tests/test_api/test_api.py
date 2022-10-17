from elasticsearch import AsyncElasticsearch, NotFoundError
from httpx import AsyncClient
import pytest
from redis.asyncio import Redis


@pytest.mark.asyncio
async def test_search_posts(client: AsyncClient, redis: Redis):
    response = await client.post("/api/v1/search", json={"text": "test"})
    redis_response = await redis.get("test")

    assert response.status_code == 200
    assert redis_response is not None
    assert len(response.json()) == 10


@pytest.mark.asyncio
async def test_delete_post(client: AsyncClient, es: AsyncElasticsearch):
    data = await es.search(index="posts", query={"match": {"text": "test"}})
    id: str = data.body["hits"]["hits"][0]["_id"]

    assert id is not None
    response = await client.delete(f"/api/v1/delete/{id}")
    try:
        deleted_item = await es.get(index="posts", id=id)
    except NotFoundError:
        deleted_item = None

    assert response.status_code == 200
    assert deleted_item == None


@pytest.mark.asyncio
async def test_get_post(client: AsyncClient, es: AsyncElasticsearch):
    data = await es.search(index="posts", query={"match": {"text": "test"}})
    id: str = data.body["hits"]["hits"][1]["_id"]
    response = await client.get(f"/api/v1/post/{id}")

    assert response.status_code == 200
    assert response.json()["id"] == id
