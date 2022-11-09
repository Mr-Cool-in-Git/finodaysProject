from fastapi import APIRouter
from .api import router as api_router
#from .budgets import router as budgets_router

router = APIRouter()

router.include_router(api_router)
#router.include_router(operations_router)
#router.include_router(budgets_router)

