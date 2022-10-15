from datetime import datetime
import orjson
from pydantic import BaseModel


class DocumentId(BaseModel):
    id: str


class DocumentIn(BaseModel):
    text: str


class Document(DocumentId, DocumentIn):
    created_date: datetime
    rubrics: list[str]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps
