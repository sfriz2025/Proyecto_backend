from typing import Literal, Optional

from fastapi import APIRouter, Depends, Path, Query, Response, status

from App.core.errors import ErrorResponse
from App.core.pagination import Pagina
from App.presentation.schemas.platillos_shemas import PlatilloCreate, PlatilloResponse, PlatilloUpdate
from App.Application.dtos.platillos_query_dto import PlatilloQuery
from App.Application.services.platillos_services import PlatilloService, get_platillo_service

router = APIRouter(prefix="/platillos", tags=["Platillos"])

R404 = {404: {"model": ErrorResponse, "description": "El platillo no existe"}}
R409 = {409: {"model": ErrorResponse, "description": "Conflicto con el estado actual"}}
R422 = {422: {"model": ErrorResponse, "description": "Datos inválidos"}}


@router.get(
    "",
    response_model=Pagina[PlatilloResponse],
    summary="Listar platillos",
    description="Filtra por categoría, ordena y pagina (en ese orden).",
    responses=R422,
)
def listar_platillos(
    categoria: Optional[str] = Query(None, description="Categoría exacta", examples=["pastas"]),
    ordenar_por: Literal["id", "nombre", "precio_restaurante", "tiempo_restaurante_min"] = Query("id"),
    direccion: Literal["asc", "desc"] = Query("asc"),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    service: PlatilloService = Depends(get_platillo_service),
):
    return service.listar(PlatilloQuery(categoria, ordenar_por, direccion, pagina, limite))


@router.post(
    "",
    response_model=PlatilloResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear platillo",
    description="Crea un platillo. El nombre no puede repetirse.",
    responses={**R409, **R422},
)
def crear_platillo(datos: PlatilloCreate, service: PlatilloService = Depends(get_platillo_service)):
    return service.crear(datos)


@router.get(
    "/{platillo_id}",
    response_model=PlatilloResponse,
    summary="Obtener platillo por ID",
    responses={**R404, **R422},
)
def obtener_platillo(
    platillo_id: int = Path(..., ge=1),
    service: PlatilloService = Depends(get_platillo_service),
):
    return service.obtener(platillo_id)


@router.patch(
    "/{platillo_id}",
    response_model=PlatilloResponse,
    summary="Actualizar platillo",
    description="Actualiza solo los campos enviados.",
    responses={**R404, **R409, **R422},
)
def actualizar_platillo(
    datos: PlatilloUpdate,
    platillo_id: int = Path(..., ge=1),
    service: PlatilloService = Depends(get_platillo_service),
):
    return service.actualizar(platillo_id, datos)


@router.delete(
    "/{platillo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Eliminar platillo",
    description="No se puede eliminar un platillo con pedidos activos.",
    responses={**R404, **R409},
)
def eliminar_platillo(
    platillo_id: int = Path(..., ge=1),
    service: PlatilloService = Depends(get_platillo_service),
):
    service.eliminar(platillo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
