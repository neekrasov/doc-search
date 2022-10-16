from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_post_service
from services.posts import PostService
from schemas.posts import Post, PostIn

router = APIRouter(prefix="", tags=["doc"])


@router.post("/search", response_model=list[Post])
async def search_posts(
    post: PostIn,
    post_service: PostService = Depends(get_post_service),
):
    posts = await post_service.search_posts(post.text)
    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    return posts


@router.delete("/delete/{post_id}")
async def delete_post(
    post_id: str,
    post_service: PostService = Depends(get_post_service),
):
    status = await post_service.delete_post(post_id)
    if not status:
        raise HTTPException(status_code=404, detail="Post not found")


@router.get("/post/{post_id}", response_model=Post)
async def get_post(
    post_id: str,
    post_service: PostService = Depends(get_post_service),
):
    post = await post_service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
