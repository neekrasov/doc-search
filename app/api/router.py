from fastapi import APIRouter
from .v1.doc import router as v1_doc_router

router = APIRouter(prefix="/v1")
router.include_router(v1_doc_router)
