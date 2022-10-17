import asyncio
import json
import pytest_asyncio
from httpx import AsyncClient
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch

from app.main import app
from app.core.settings import Settings, get_settings


@pytest_asyncio.fixture(scope="session")
async def fill_test_data(es: AsyncElasticsearch):

    if await es.indices.exists(index="posts"):
        await es.indices.delete(index="posts", ignore=[400, 404])
    with open("../tests/json/test_mappings.json", "r") as f:
        mappings = json.load(f)
    await es.indices.create(index="posts", mappings=mappings)

    with open("../tests/json/test_data.json", "r") as f:
        posts = json.load(f)
    for post in posts:
        await es.index(index="posts", document=post)


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def settings():
    return get_settings()


@pytest_asyncio.fixture
async def redis(settings: Settings):
    redis = Redis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")
    yield redis
    await redis.close()


@pytest_asyncio.fixture
async def es(settings: Settings):
    es = AsyncElasticsearch(f"http://{settings.elastic_host}:{settings.elastic_port}")
    yield es
    await es.close()


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://test",
    ) as client:
        yield client
