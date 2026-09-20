# app/main.py
from fastapi import FastAPI
from app.api.api_v1.api import api_router

app = FastAPI(
    title="Food Cart API - Mi Carrito de Comida",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs"  # --- Swagger UI ---
)

app.include_router(api_router, prefix="/api/v1")