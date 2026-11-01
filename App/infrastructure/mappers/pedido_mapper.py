from App.domain.pedidos_domain import EstadoPedido, Modalidad, Pedido
from App.infrastructure.models import PedidoModel


def pedido_a_dominio(modelo: PedidoModel) -> Pedido:
    return Pedido(
        id=modelo.id,
        cuenta_id=modelo.cuenta_id,
        platillo_id=modelo.platillo_id,
        modalidad=Modalidad(modelo.modalidad),
        cantidad=modelo.cantidad,
        estado=EstadoPedido(modelo.estado),
        fecha=modelo.fecha,
        total=modelo.total,
    )

def pedido_a_modelo(pedido: Pedido) -> PedidoModel:
    return PedidoModel(
        id=pedido.id if pedido.id > 0 else None,
        cuenta_id=pedido.cuenta_id,
        platillo_id=pedido.platillo_id,
        modalidad=pedido.modalidad.value,
        cantidad=pedido.cantidad,
        estado=pedido.estado.value,
        fecha=pedido.fecha,
        total=pedido.total,
    )
