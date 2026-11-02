from sqlalchemy import delete, extract, func, select
from sqlalchemy.orm import Session

from domain.pedidos_domain import EstadoPedido, Pedido
from infrastructure.mappers.pedido_mapper import (
    pedido_a_dominio,
    pedido_a_modelo,
)
from infrastructure.models import PedidoModel

class PedidoSQLRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, pedido_id: int) -> Pedido | None:
        modelo = self.db.get(PedidoModel, pedido_id)

        if modelo is None:
            return None

        return pedido_a_dominio(modelo)

    def get_all(self) -> list[Pedido]:
        modelos = self.db.scalars(select(PedidoModel)).all()
        return [pedido_a_dominio(modelo) for modelo in modelos]

    def add(self, pedido: Pedido) -> Pedido:
        modelo = pedido_a_modelo(pedido)
        self.db.add(modelo)

        try:
            self.db.commit()
            self.db.refresh(modelo)
        except Exception:
            self.db.rollback()
            raise

        return pedido_a_dominio(modelo)

    def update(self, pedido_id: int, pedido: Pedido) -> Pedido | None:
        modelo = self.db.get(PedidoModel, pedido_id)
        if modelo is None:
            return None


        modelo.cuenta_id = pedido.cuenta_id
        modelo.platillo_id = pedido.platillo_id
        modelo.modalidad = pedido.modalidad.value
        modelo.cantidad = pedido.cantidad
        modelo.estado = pedido.estado.value
        modelo.fecha = pedido.fecha
        modelo.total = pedido.total

        try:
            self.db.commit()
            self.db.refresh(modelo)
        except Exception:
            self.db.rollback()
            raise

        return pedido_a_dominio(modelo)

    def gasto_del_mes(self, cuenta_id: int, anio: int, mes: int) -> float:
        consulta = select(func.sum(PedidoModel.total)).where(
            PedidoModel.cuenta_id == cuenta_id,
            PedidoModel.estado != EstadoPedido.CANCELADO.value,
            extract("year", PedidoModel.fecha) == anio,
            extract("month", PedidoModel.fecha) == mes,
        )
        total = self.db.scalar(consulta) or 0
        return round(float(total), 2)

    def tiene_activos_de_cuenta(self, cuenta_id: int) -> bool:
        estados_activos = [
            EstadoPedido.PENDIENTE.value,
            EstadoPedido.CONFIRMADO.value,
        ]
        consulta = (
            select(PedidoModel.id)
            .where(
                PedidoModel.cuenta_id == cuenta_id,
                PedidoModel.estado.in_(estados_activos),
            )
            .limit(1)
        )
        return self.db.scalar(consulta) is not None


    def tiene_activos_de_platillo(self, platillo_id: int) -> bool:
        estados_activos = [
            EstadoPedido.PENDIENTE.value,
            EstadoPedido.CONFIRMADO.value,
        ]
        consulta = (
            select(PedidoModel.id)
            .where(
                PedidoModel.platillo_id == platillo_id,
                PedidoModel.estado.in_(estados_activos),
            )
            .limit(1)
        )
        return self.db.scalar(consulta) is not None

    def eliminar_por_cuenta(self, cuenta_id: int) -> None:
        consulta = delete(PedidoModel).where(PedidoModel.cuenta_id == cuenta_id)

        try:
            self.db.execute(consulta)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
