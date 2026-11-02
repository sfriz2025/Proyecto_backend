from typing import Literal, Optional

from fastapi import APIRouter, Depends, Path, Query, Response, status

from App.core.errors import ErrorResponse
from App.core.pagination import Pagina
from App.presentation.schemas.cuentas_shemas import (
    CuentaCreate,
    CuentaResponse,
    CuentaUpdate,
    ResumenCuentaResponse,
)
from App.Application.services.cuentas_services import CuentaService, get_cuenta_service
from App.Application.dtos.cuentas_query_dto import CuentaQuery

router = APIRouter(prefix="/cuentas", tags=["Cuentas"])

R404 = {404: {"model": ErrorResponse, "description": "La cuenta no existe"}}
R409 = {409: {"model": ErrorResponse, "description": "Conflicto con el estado actual"}}
R422 = {422: {"model": ErrorResponse, "description": "Datos inválidos"}}


@router.get(
    "",
    response_model=Pagina[CuentaResponse],
    summary="Listar cuentas",
    description="Filtra por texto en el nombre del titular, ordena y pagina (en ese orden).",
    responses=R422,
)
def listar_cuentas(
    nombre: Optional[str] = Query(None, description="Texto contenido en el nombre del titular"),
    ordenar_por: Literal["id", "nombre_titular", "presupuesto_mensual", "fecha_creacion"] = Query("id"),
    direccion: Literal["asc", "desc"] = Query("asc"),
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    service: CuentaService = Depends(get_cuenta_service),
):
    return service.listar(CuentaQuery(nombre, ordenar_por, direccion, pagina, limite))


@router.post(
    "",
    response_model=CuentaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear cuenta",
    description="Crea una cuenta. El correo no puede repetirse.",
    responses={**R409, **R422},
)
def crear_cuenta(datos: CuentaCreate, service: CuentaService = Depends(get_cuenta_service)):
    return service.crear(datos)


@router.get(
    "/{cuenta_id}",
    response_model=CuentaResponse,
    summary="Obtener cuenta por ID",
    responses={**R404, **R422},
)
def obtener_cuenta(
    cuenta_id: int = Path(..., ge=1),
    service: CuentaService = Depends(get_cuenta_service),
):
    return service.obtener(cuenta_id)


@router.get(
    "/{cuenta_id}/resumen",
    response_model=ResumenCuentaResponse,
    summary="Resumen de gasto del mes",
    description="Presupuesto, gasto del mes (sin pedidos cancelados) y saldo disponible.",
    responses={**R404, **R422},
)
def resumen_cuenta(
    cuenta_id: int = Path(..., ge=1),
    service: CuentaService = Depends(get_cuenta_service),
):
    return service.resumen(cuenta_id)


@router.patch(
    "/{cuenta_id}",
    response_model=CuentaResponse,
    summary="Actualizar cuenta",
    description="Actualiza solo los campos enviados.",
    responses={**R404, **R409, **R422},
)
def actualizar_cuenta(
    datos: CuentaUpdate,
    cuenta_id: int = Path(..., ge=1),
    service: CuentaService = Depends(get_cuenta_service),
):
    return service.actualizar(cuenta_id, datos)


@router.delete(
    "/{cuenta_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Eliminar cuenta",
    description="No se puede eliminar una cuenta con pedidos activos (pendientes o confirmados).",
    responses={**R404, **R409},
)
def eliminar_cuenta(
    cuenta_id: int = Path(..., ge=1),
    service: CuentaService = Depends(get_cuenta_service),
):
    service.eliminar(cuenta_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
