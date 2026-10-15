from typing import Literal, Optional

from fastapi import APIRouter, Depends, Path, Query, status

from App.core.errors import ErrorResponse
from App.core.pagination import Pagina
from App.domain.pedidos_domain import EstadoPedido
from App.schemas.pedidos_shemas import PedidoCreate, PedidoEstadoUpdate, PedidoResponse
from App.services.dtos.pedidos_query_dto import PedidoQuery
from App.services.pedidos_services import PedidoService, get_pedido_service

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

R400 = {400: {"model": ErrorResponse, "description": "Viola una regla de negocio"}}
R404 = {404: {"model": ErrorResponse, "description": "El recurso no existe"}}
R422 = {422: {"model": ErrorResponse, "description": "Datos inválidos"}}


@router.get(
    "",
    response_model=Pagina[PedidoResponse],
    summary="Listar pedidos",
    description="Filtra por estado y/o cuenta, ordena y pagina (en ese orden).",
    responses=R422,
)
def listar_pedidos(
    estado: Optional[EstadoPedido] = Query(None),
    cuenta_id: Optional[int] = Query(None, ge=1),
    ordenar_por: Literal["id", "fecha", "total", "cantidad"] = Query("id"),
    direccion: Literal["asc", "desc"] = Query("asc"),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    service: PedidoService = Depends(get_pedido_service),
):
    return service.listar(PedidoQuery(estado, cuenta_id, ordenar_por, direccion, pagina, limite))


@router.post(
    "",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear pedido",
    description=(
        "Crea un pedido en estado 'pendiente'. El total lo calcula el servidor según la "
        "modalidad. Falla si la cuenta o el platillo no existen (404) o si el pedido supera "
        "el presupuesto mensual de la cuenta (400)."
    ),
    responses={**R400, **R404, **R422},
)
def crear_pedido(datos: PedidoCreate, service: PedidoService = Depends(get_pedido_service)):
    return service.crear(datos)


@router.get(
    "/{pedido_id}",
    response_model=PedidoResponse,
    summary="Obtener pedido por ID",
    responses={**R404, **R422},
)
def obtener_pedido(
    pedido_id: int = Path(..., ge=1),
    service: PedidoService = Depends(get_pedido_service),
):
    return service.obtener(pedido_id)


@router.patch(
    "/{pedido_id}/estado",
    response_model=PedidoResponse,
    summary="Cambiar estado del pedido",
    description="Flujo permitido: pendiente → confirmado → entregado. Se puede cancelar desde pendiente o confirmado.",
    responses={**R400, **R404, **R422},
)
def cambiar_estado_pedido(
    datos: PedidoEstadoUpdate,
    pedido_id: int = Path(..., ge=1),
    service: PedidoService = Depends(get_pedido_service),
):
    return service.cambiar_estado(pedido_id, datos.estado)


@router.delete(
    "/{pedido_id}",
    response_model=PedidoResponse,
    summary="Cancelar pedido",
    description="Cancela el pedido (queda registrado como 'cancelado'). Solo si está pendiente o confirmado.",
    responses={**R400, **R404, **R422},
)
def cancelar_pedido(
    pedido_id: int = Path(..., ge=1),
    service: PedidoService = Depends(get_pedido_service),
):
    return service.cancelar(pedido_id)
