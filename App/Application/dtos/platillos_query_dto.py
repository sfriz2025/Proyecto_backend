from dataclasses import dataclass
from typing import Optional


@dataclass
class PlatilloQuery:
    categoria: Optional[str] = None
    ordenar_por: str = "id"
    direccion: str = "asc"
    pagina: int = 1
    limite: int = 10
