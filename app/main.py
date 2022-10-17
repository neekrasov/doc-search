import logging
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis
import uvicorn
from fastapi import FastAPI

from fastapi.responses import ORJSONResponse
from core.settings import get_settings
from core.logger import LOGGING
from api.router import router as api_router
from api.dependencies import get_redis, get_elastic


def create_app() -> FastAPI:

    settings = get_settings()

    app = FastAPI(
        title=settings.project_name,
        description=settings.descriprion,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )

    redis = Redis.from_url(url=f"redis://{settings.redis_host}:{settings.redis_port}")

    logging.info("Redis: connection established")

    elastic = AsyncElasticsearch(
        hosts=[f"http://{settings.elastic_host}:{settings.elastic_port}"]
    )

    logging.info("Elasticsearch: connection established")

    app.dependency_overrides[get_redis] = lambda: redis
    app.dependency_overrides[get_elastic] = lambda: elastic
    app.include_router(api_router, prefix=settings.api_prefix)

    async def shutdown():
        await redis.close()
        await elastic.close()

    app.add_event_handler("shutdown", shutdown)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
