from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Modalidad(str, Enum):
    RESTAURANTE = "restaurante"
    CASA = "casa"


class EstadoPedido(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


# Regla de negocio: flujo permitido de estados.
TRANSICIONES = {
    EstadoPedido.PENDIENTE: {EstadoPedido.CONFIRMADO, EstadoPedido.CANCELADO},
    EstadoPedido.CONFIRMADO: {EstadoPedido.ENTREGADO, EstadoPedido.CANCELADO},
    EstadoPedido.ENTREGADO: set(),
    EstadoPedido.CANCELADO: set(),
}

ESTADOS_ACTIVOS = {EstadoPedido.PENDIENTE, EstadoPedido.CONFIRMADO}


@dataclass
class Pedido:
    """Pedido de una cuenta para un platillo."""

    id: int
    cuenta_id: int
    platillo_id: int
    modalidad: Modalidad
    cantidad: int
    estado: EstadoPedido
    fecha: datetime
    total: float

    def puede_pasar_a(self, nuevo: EstadoPedido) -> bool:
        return nuevo in TRANSICIONES[self.estado]

    def esta_activo(self) -> bool:
        return self.estado in ESTADOS_ACTIVOS
