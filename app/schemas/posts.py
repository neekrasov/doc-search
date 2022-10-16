from datetime import datetime
import orjson
from pydantic import BaseModel


class PostId(BaseModel):
    id: str


class PostIn(BaseModel):
    text: str


class Post(PostId, PostIn):
    created_date: datetime
    rubrics: list[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps
