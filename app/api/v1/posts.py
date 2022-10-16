from fastapi import APIRouter, Depends, HTTPException, status
from schemas.posts import Post, PostIn

router = APIRouter(prefix="", tags=["doc"])


@router.get("/search", response_model=list[Post])
async def search_posts():
    pass
