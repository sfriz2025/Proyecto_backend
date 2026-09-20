# app/api/api_v1/endpoints/productos.py
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.services.producto_service import ProductoService
from app.schemas.producto import ProductoResponse, ProductoCreate

router = APIRouter()

# Inyección del servicio
def get_producto_service() -> ProductoService:
    return ProductoService()

@router.get("/", response_model=List[ProductoResponse])
async def read_productos(skip: int = 0, limit: int = 10, service: ProductoService = Depends(get_producto_service)):
    # Capa de Códigos HTTP: 200 OK (por defecto)
    return service.get_productos(skip=skip, limit=limit)

@router.post("/", response_model=ProductoResponse)
async def create_producto(producto_in: ProductoCreate, service: ProductoService = Depends(get_producto_service)):
    # Capa de Códigos HTTP: 201 Created
    try:
        producto_creado = service.create_producto(producto_in)
        return producto_creado
    except ValueError as e:
        # Capa de Códigos HTTP: 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))