from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from App.schemas.platillo import PlatilloCreate, PlatilloResponse, PlatilloUpdate
from App.services.platillo_service import PlatilloService

router = APIRouter() 
service = PlatilloService()

@router.get("/", response_model=List[PlatilloResponse], status_code=status.HTTP_200_OK)
async def listar_platillos(
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    ordenar_por: Optional[str] = Query(None, description="Opciones: precio, ahorro_tiempo"),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=50)
):
    """Obtiene el catálogo con comparativa y soporte de filtro/orden/paginación."""
    return service.obtener_platillos(categoria, ordenar_por, pagina, limite)

@router.post("/", response_model=PlatilloResponse, status_code=status.HTTP_201_CREATED)
async def crear_platillo(platillo_in: PlatilloCreate):
    """Crea un nuevo platillo en el catálogo."""
    try:
        return service.crear_platillo(platillo_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{platillo_id}", response_model=PlatilloResponse, status_code=status.HTTP_200_OK)
async def obtener_platillo(platillo_id: int):
    platillo = service.obtener_platillo(platillo_id)
    if platillo is None:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    return platillo

@router.put("/{platillo_id}", response_model=PlatilloResponse, status_code=status.HTTP_200_OK)
async def actualizar_platillo(platillo_id: int, datos: PlatilloUpdate):
    platillo = service.actualizar_platillo(platillo_id, datos)
    if platillo is None:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    return platillo

@router.delete("/{platillo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_platillo(platillo_id: int):
    eliminado = service.eliminar_platillo(platillo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    return None
