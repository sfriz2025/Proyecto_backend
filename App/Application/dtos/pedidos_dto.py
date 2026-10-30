from dataclasses import dataclass


@dataclass
class CalculoPedidoDTO:
    """Precio unitario según la modalidad y total calculado por el servidor."""

    precio_unitario: float
    total: float
