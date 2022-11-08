from fastapi import APIRouter
from .operations import router as operations_router
from .budgets import router as budgets_router

router = APIRouter()

#router.include_router(operations_router)
router.include_router(budgets_router)

