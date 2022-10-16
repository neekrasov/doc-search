from datetime import datetime
import orjson
from pydantic import BaseModel
from pydantic import validator


class PostId(BaseModel):
    id: str


class PostIn(BaseModel):
    text: str


class Post(PostId, PostIn):
    created_date: datetime
    rubrics: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps
