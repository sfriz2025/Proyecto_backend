from App.domain.pedidos_domain import EstadoPedido, Pedido
from App.Infraestructure.repositories.base_repo import InMemoryRepository


class PedidoRepository(InMemoryRepository[Pedido]):
    def tiene_activos_de_platillo(self, platillo_id: int) -> bool:
        return any(p.platillo_id == platillo_id and p.esta_activo() for p in self._items.values())

    def tiene_activos_de_cuenta(self, cuenta_id: int) -> bool:
        return any(p.cuenta_id == cuenta_id and p.esta_activo() for p in self._items.values())

    def eliminar_por_cuenta(self, cuenta_id: int) -> None:
        for p in [p for p in self._items.values() if p.cuenta_id == cuenta_id]:
            self._items.pop(p.id, None)

    def gasto_del_mes(self, cuenta_id: int, anio: int, mes: int) -> float:
        """Suma los pedidos no cancelados de la cuenta en ese mes."""
        return round(
            sum(
                p.total
                for p in self._items.values()
                if p.cuenta_id == cuenta_id
                and p.estado != EstadoPedido.CANCELADO
                and p.fecha.year == anio
                and p.fecha.month == mes
            ),
            2,
        )


pedido_repo = PedidoRepository()
