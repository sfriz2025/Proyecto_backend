from dataclasses import dataclass
from typing import Optional

from domain.productos_domain import Unidad


@dataclass
class ProductoQuery:
    unidad: Optional[Unidad] = None
    ordenar_por: str = "id"
    direccion: str = "asc"
    pagina: int = 1
    limite: int = 10
