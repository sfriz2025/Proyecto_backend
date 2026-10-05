from fastapi import APIRouter
from .endpoints import platillos

api_router = APIRouter()
api_router.include_router(platillos.router, prefix="/platillos", tags=["Platillos"])