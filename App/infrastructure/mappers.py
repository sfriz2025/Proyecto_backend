from App.domain.cuentas_domain import Cuenta
from App.domain.pedidos_domain import Pedido
from App.domain.platillos_domain import Platillo
from App.domain.productos_domain import Producto
from App.infrastructure.models.orm import CuentaORM, PedidoORM, PlatilloORM, ProductoORM


def to_domain(row, cls):
    return cls(**{column.name: getattr(row, column.name) for column in row.__table__.columns})


def cuenta_to_orm(value: Cuenta) -> CuentaORM:
    return CuentaORM(**vars(value))


def platillo_to_orm(value: Platillo) -> PlatilloORM:
    return PlatilloORM(**vars(value))


def producto_to_orm(value: Producto) -> ProductoORM:
    return ProductoORM(**vars(value))


def pedido_to_orm(value: Pedido) -> PedidoORM:
    return PedidoORM(**vars(value))
