from dataclasses import asdict
from datetime import datetime
from typing import Optional

from App.core.errors import BusinessRuleError, ConflictError, NotFoundError
from fastapi import Depends
from sqlalchemy.orm import Session

from App.core.pagination import construir_pagina, ordenar, paginar
from App.domain.cuentas_domain import Cuenta
from App.infrastructure.database import get_db
from App.infrastructure.repositories.cuentas_repository import CuentaSQLRepository
from App.repositories.cuentas_repo import CuentaRepository, cuenta_repo
from App.repositories.pedidos_repo import PedidoRepository, pedido_repo
from App.schemas.cuentas_shemas import (
    CuentaCreate,
    CuentaResponse,
    CuentaUpdate,
    ResumenCuentaResponse,
)
from App.services.dtos.cuentas_dto import ResumenGastoDTO
from App.services.dtos.cuentas_query_dto import CuentaQuery


class CuentaService:
    def __init__(
        self,
        repo: Optional[CuentaRepository] = None,
        pedidos: Optional[PedidoRepository] = None,
    ):
        self.repo = repo if repo is not None else cuenta_repo
        self.pedidos = pedidos if pedidos is not None else pedido_repo

    # ---------- utilidades ----------
    def _obtener_o_404(self, cuenta_id: int) -> Cuenta:
        cuenta = self.repo.get(cuenta_id)
        if cuenta is None:
            raise NotFoundError("No existe una cuenta con el ID solicitado")
        return cuenta

    def _validar_correo_unico(self, correo: str, ignorar_id: Optional[int] = None) -> None:
        existente = self.repo.buscar_por_correo(correo)
        if existente is not None and existente.id != ignorar_id:
            raise ConflictError(
                "Ya existe una cuenta con ese correo",
                [{"campo": "correo", "mensaje": "El correo ya está registrado"}],
            )

    # ---------- casos de uso ----------
    def listar(self, q: CuentaQuery) -> dict:
        listar_sql = getattr(self.repo, "listar", None)
        if listar_sql is not None:
            pagina, total = listar_sql(
                q.nombre, q.ordenar_por, q.direccion, q.pagina, q.limite
            )
        else:
            cuentas = self.repo.get_all()
            if q.nombre:
                cuentas = [c for c in cuentas if q.nombre.lower() in c.nombre_titular.lower()]
            cuentas = ordenar(cuentas, q.ordenar_por, q.direccion)
            total = len(cuentas)
            pagina = paginar(cuentas, q.pagina, q.limite)
        items = [CuentaResponse.model_validate(c) for c in pagina]
        return construir_pagina(items, total, q.pagina, q.limite)

    def crear(self, datos: CuentaCreate) -> CuentaResponse:
        correo = datos.correo.strip().lower()
        self._validar_correo_unico(correo)
        cuenta = self.repo.add(
            Cuenta(
                id=0,
                nombre_titular=datos.nombre_titular,
                correo=correo,
                presupuesto_mensual=datos.presupuesto_mensual,
                fecha_creacion=datetime.now(),
            )
        )
        return CuentaResponse.model_validate(cuenta)

    def obtener(self, cuenta_id: int) -> CuentaResponse:
        return CuentaResponse.model_validate(self._obtener_o_404(cuenta_id))

    def actualizar(self, cuenta_id: int, datos: CuentaUpdate) -> CuentaResponse:
        actual = self._obtener_o_404(cuenta_id)
        cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
        if "presupuesto_mensual" in cambios:
            hoy = datetime.now()
            gasto = self.pedidos.gasto_del_mes(cuenta_id, hoy.year, hoy.month)

            if cambios["presupuesto_mensual"] < gasto:
                raise BusinessRuleError(
                    "El presupuesto no puede ser menor que el gasto del mes",
                    [
                        {
                            "presupuesto_mensual": cambios["presupuesto_mensual"],
                            "gasto_mes": gasto,
                        }
                    ],
                )
        if "correo" in cambios:
            cambios["correo"] = cambios["correo"].strip().lower()
            self._validar_correo_unico(cambios["correo"], ignorar_id=cuenta_id)
        actualizada = self.repo.update(cuenta_id, Cuenta(**{**asdict(actual), **cambios}))
        return CuentaResponse.model_validate(actualizada)

    def eliminar(self, cuenta_id: int) -> None:
        self._obtener_o_404(cuenta_id)
        # Regla de negocio: no se elimina una cuenta con pedidos activos.
        if self.pedidos.tiene_activos_de_cuenta(cuenta_id):
            raise ConflictError("No se puede eliminar una cuenta con pedidos activos")
        self.pedidos.eliminar_por_cuenta(cuenta_id)
        self.repo.delete(cuenta_id)

    def resumen(self, cuenta_id: int) -> ResumenCuentaResponse:
        cuenta = self._obtener_o_404(cuenta_id)
        hoy = datetime.now()
        gasto = self.pedidos.gasto_del_mes(cuenta_id, hoy.year, hoy.month)
        dto = ResumenGastoDTO(
            cuenta_id=cuenta.id,
            presupuesto_mensual=cuenta.presupuesto_mensual,
            gasto_mes=gasto,
            disponible=round(cuenta.presupuesto_mensual - gasto, 2),
        )
        return ResumenCuentaResponse(**asdict(dto))


def get_cuenta_service(db: Session = Depends(get_db)) -> CuentaService:
    return CuentaService(repo=CuentaSQLRepository(db))
