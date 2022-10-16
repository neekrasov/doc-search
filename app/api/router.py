from fastapi import APIRouter
from .v1.posts import router as v1_posts_router

router = APIRouter(prefix="/v1")
router.include_router(v1_posts_router)
