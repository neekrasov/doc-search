from fastapi import APIRouter, Depends, HTTPException, status
from schemas.doc import Document, DocumentIn

router = APIRouter(prefix="", tags=["doc"])


@router.get("/search", response_model=list[Document])
async def search_documents():
    pass
