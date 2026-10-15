from dataclasses import dataclass
from enum import Enum


class Unidad(str, Enum):
    GRAMO = "g"
    KILO = "kg"
    LITRO = "l"
    MILILITRO = "ml"
    UNIDAD = "unidad"


@dataclass
class Producto:
    """Ingrediente de un platillo. Un platillo tiene muchos productos (1:N)."""

    id: int
    platillo_id: int
    nombre: str
    cantidad: float
    unidad: Unidad
    precio_unitario: float

    def costo_total(self) -> float:
        return round(self.cantidad * self.precio_unitario, 2)
