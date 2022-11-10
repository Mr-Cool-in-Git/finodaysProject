from fastapi import APIRouter
from .histories import router as histories_router
from .accounts import router as accounts_router
from .clients import router as clients_router

router = APIRouter()

router.include_router(histories_router)
router.include_router(accounts_router)
router.include_router(clients_router)

