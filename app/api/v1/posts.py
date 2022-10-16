from fastapi import APIRouter, Depends
from api.dependencies import get_post_service
from services.posts import PostService
from schemas.posts import Post, PostIn

router = APIRouter(prefix="", tags=["doc"])


@router.post("/search", response_model=list[Post])
async def search_posts(
    post: PostIn,
    post_sevice: PostService = Depends(get_post_service),
):
    posts = await post_sevice.get_posts(post.text)
    if posts is None:
        return []
    return posts
