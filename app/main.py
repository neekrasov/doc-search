import logging
import uvicorn
from fastapi import FastAPI

from fastapi.responses import ORJSONResponse
from core.settings import get_settings
from core.logger import LOGGING
from api.router import router as api_router
from db import events as db_events

settings = get_settings()

app = FastAPI(
    title=settings.project_name,
    description=settings.descriprion,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    on_startup=[db_events.startup],
    on_shutdown=[db_events.shutdown],
)

app.include_router(api_router, prefix=settings.api_prefix)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
