from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "Doc-search"
    descriprion: str = "Document search engine"
    redis_host: str = "localhost"
    redis_port: int = 6379
    elastic_host: str = "localhost"
    elastic_port: int = 9200
    api_prefix: str = "/api"

    class Config:
        env_file = "dev.env"


@lru_cache()
def get_settings(**kwargs):
    return Settings(**kwargs)
