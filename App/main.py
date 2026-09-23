from fastapi import FastAPI
from .api.api_v1.api import api_router

app = FastAPI(
    title="Restaurante vs Casa API",
    description="API REST que compara costo y tiempo de comer en local vs cocinar en casa",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")