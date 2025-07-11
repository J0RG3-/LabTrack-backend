from fastapi import APIRouter
from .user_router import router as user_router
from .compound_router import router as compound_router
from .compound_instance_router import router as instance_router
from .transaction_router import router as transaction_router
from .count_session_router import router as count_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(compound_router)
api_router.include_router(instance_router)
api_router.include_router(transaction_router)
api_router.include_router(count_router)
