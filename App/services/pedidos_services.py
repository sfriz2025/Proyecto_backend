from dataclasses import asdict
from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from App.core.errors import BusinessRuleError, NotFoundError
from App.core.pagination import construir_pagina, ordenar, paginar
from App.domain.pedidos_domain import EstadoPedido, Modalidad, Pedido
from App.domain.platillos_domain import Platillo
from App.infrastructure.database import get_db
from App.infrastructure.repositories.cuentas_repository import CuentaSQLRepository
from App.repositories.cuentas_repo import CuentaRepository, cuenta_repo
from App.repositories.pedidos_repo import PedidoRepository, pedido_repo
from App.repositories.platillos_repo import PlatilloRepository, platillo_repo
from App.schemas.pedidos_shemas import PedidoCreate, PedidoResponse
from App.services.dtos.pedidos_dto import CalculoPedidoDTO
from App.services.dtos.pedidos_query_dto import PedidoQuery


class PedidoService:
    def __init__(
        self,
        repo: Optional[PedidoRepository] = None,
        cuentas: Optional[CuentaRepository] = None,
        platillos: Optional[PlatilloRepository] = None,
    ):
        self.repo = repo if repo is not None else pedido_repo
        self.cuentas = cuentas if cuentas is not None else cuenta_repo
        self.platillos = platillos if platillos is not None else platillo_repo

    # ---------- utilidades ----------
    def _obtener_o_404(self, pedido_id: int) -> Pedido:
        pedido = self.repo.get(pedido_id)
        if pedido is None:
            raise NotFoundError("No existe un pedido con el ID solicitado")
        return pedido

    @staticmethod
    def _calcular(platillo: Platillo, modalidad: Modalidad, cantidad: int) -> CalculoPedidoDTO:
        """Regla de negocio: el total lo calcula el servidor según la modalidad."""
        if modalidad == Modalidad.RESTAURANTE:
            unitario = platillo.precio_restaurante
        else:
            unitario = platillo.costo_estimado_casa
        return CalculoPedidoDTO(precio_unitario=unitario, total=round(unitario * cantidad, 2))

    # ---------- casos de uso ----------
    def listar(self, q: PedidoQuery) -> dict:
        pedidos = self.repo.get_all()
        if q.estado is not None:
            pedidos = [p for p in pedidos if p.estado == q.estado]
        if q.cuenta_id is not None:
            pedidos = [p for p in pedidos if p.cuenta_id == q.cuenta_id]
        pedidos = ordenar(pedidos, q.ordenar_por, q.direccion)
        total = len(pedidos)
        pagina = paginar(pedidos, q.pagina, q.limite)
        items = [PedidoResponse(**asdict(p)) for p in pagina]
        return construir_pagina(items, total, q.pagina, q.limite)

    def crear(self, datos: PedidoCreate) -> PedidoResponse:
        # Validación de existencia relacionada -> 404
        cuenta = self.cuentas.get(datos.cuenta_id)
        if cuenta is None:
            raise NotFoundError("No existe una cuenta con el ID solicitado")
        platillo = self.platillos.get(datos.platillo_id)
        if platillo is None:
            raise NotFoundError("No existe un platillo con el ID solicitado")

        calculo = self._calcular(platillo, datos.modalidad, datos.cantidad)

        # Regla de negocio: el gasto del mes no puede superar el presupuesto de la cuenta.
        ahora = datetime.now()
        gasto_actual = self.repo.gasto_del_mes(cuenta.id, ahora.year, ahora.month)
        if gasto_actual + calculo.total > cuenta.presupuesto_mensual:
            raise BusinessRuleError(
                "El pedido supera el presupuesto mensual de la cuenta",
                [
                    {
                        "presupuesto_mensual": cuenta.presupuesto_mensual,
                        "gasto_actual": gasto_actual,
                        "total_pedido": calculo.total,
                    }
                ],
            )

        pedido = self.repo.add(
            Pedido(
                id=0,
                cuenta_id=cuenta.id,
                platillo_id=platillo.id,
                modalidad=datos.modalidad,
                cantidad=datos.cantidad,
                estado=EstadoPedido.PENDIENTE,
                fecha=ahora,
                total=calculo.total,
            )
        )
        return PedidoResponse(**asdict(pedido))

    def obtener(self, pedido_id: int) -> PedidoResponse:
        return PedidoResponse(**asdict(self._obtener_o_404(pedido_id)))

    def cambiar_estado(self, pedido_id: int, nuevo: EstadoPedido) -> PedidoResponse:
        pedido = self._obtener_o_404(pedido_id)
        # Regla de negocio: solo se permiten ciertas transiciones de estado.
        if not pedido.puede_pasar_a(nuevo):
            raise BusinessRuleError(
                f"No se puede pasar un pedido de '{pedido.estado.value}' a '{nuevo.value}'"
            )
        pedido.estado = nuevo
        return PedidoResponse(**asdict(pedido))

    def cancelar(self, pedido_id: int) -> PedidoResponse:
        """DELETE /pedidos/{id}: cancela el pedido (queda registrado como 'cancelado')."""
        return self.cambiar_estado(pedido_id, EstadoPedido.CANCELADO)


def get_pedido_service(db: Session = Depends(get_db)) -> PedidoService:
    return PedidoService(cuentas=CuentaSQLRepository(db))
