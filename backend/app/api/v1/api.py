from fastapi import APIRouter
from app.api.v1.endpoints import reports, calls, auth

api_router = APIRouter()
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(calls.router, prefix="/calls", tags=["calls"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])