from dataclasses import dataclass
from typing import Optional


@dataclass
class CuentaQuery:
    nombre: Optional[str] = None  # filtra por texto contenido en nombre_titular
    ordenar_por: str = "id"
    direccion: str = "asc"
    pagina: int = 1
    limite: int = 10
