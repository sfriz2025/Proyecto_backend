from typing import Literal, Optional

from fastapi import APIRouter, Depends, Path, Query, Response, status

from App.core.errors import ErrorResponse
from App.core.pagination import Pagina
from App.domain.productos_domain import Unidad
from App.schemas.producto_shemas import ProductoCreate, ProductoResponse
from App.services.dtos.productos_query_dto import ProductoQuery
from App.services.productos_service import ProductoService, get_producto_service

router = APIRouter(tags=["Productos"])

R404 = {404: {"model": ErrorResponse, "description": "El recurso no existe"}}
R422 = {422: {"model": ErrorResponse, "description": "Datos inválidos"}}


@router.get(
    "/platillos/{platillo_id}/productos",
    response_model=Pagina[ProductoResponse],
    summary="Listar productos (ingredientes) de un platillo",
    description="Filtra por unidad, ordena y pagina (en ese orden).",
    responses={**R404, **R422},
)
def listar_productos(
    platillo_id: int = Path(..., ge=1),
    unidad: Optional[Unidad] = Query(None),
    ordenar_por: Literal["id", "nombre", "cantidad", "precio_unitario"] = Query("id"),
    direccion: Literal["asc", "desc"] = Query("asc"),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    service: ProductoService = Depends(get_producto_service),
):
    return service.listar_por_platillo(
        platillo_id, ProductoQuery(unidad, ordenar_por, direccion, pagina, limite)
    )


@router.post(
    "/platillos/{platillo_id}/productos",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Agregar producto a un platillo",
    responses={**R404, **R422},
)
def crear_producto(
    datos: ProductoCreate,
    platillo_id: int = Path(..., ge=1),
    service: ProductoService = Depends(get_producto_service),
):
    return service.crear(platillo_id, datos)


@router.delete(
    "/productos/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Eliminar producto",
    responses=R404,
)
def eliminar_producto(
    producto_id: int = Path(..., ge=1),
    service: ProductoService = Depends(get_producto_service),
):
    service.eliminar(producto_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
