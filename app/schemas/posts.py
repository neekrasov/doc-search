from datetime import datetime
import orjson
from pydantic import BaseModel


class BasePost(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class PostId(BaseModel):
    id: str


class PostIn(BaseModel):
    text: str


class Post(PostId, PostIn, BasePost):
    created_date: datetime
    rubrics: str
