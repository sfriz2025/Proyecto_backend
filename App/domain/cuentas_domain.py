from dataclasses import dataclass
from datetime import datetime


@dataclass
class Cuenta:
    """Persona que registra sus pedidos y gastos. Una cuenta tiene muchos pedidos (1:N)."""

    id: int
    nombre_titular: str
    correo: str
    presupuesto_mensual: float
    fecha_creacion: datetime
