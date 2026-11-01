"""Ayudas comunes para filtrar -> ordenar -> paginar (sección 5.5 de la pauta)."""
from math import ceil
from typing import Any, Dict, Generic, List, Sequence, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Pagina(BaseModel, Generic[T]):
    items: List[T]
    total: int
    pagina: int
    limite: int
    total_paginas: int


def _clave(valor: Any) -> Any:
    return valor.lower() if isinstance(valor, str) else valor


def ordenar(elementos: Sequence[T], campo: str, direccion: str) -> List[T]:
    """Ordena por un atributo de la entidad. `direccion` es 'asc' o 'desc'."""
    return sorted(elementos, key=lambda e: _clave(getattr(e, campo)), reverse=(direccion == "desc"))


def paginar(elementos: Sequence[T], pagina: int, limite: int) -> List[T]:
    """`pagina` parte en 1."""
    inicio = (pagina - 1) * limite
    return list(elementos[inicio:inicio + limite])


def construir_pagina(items: list, total: int, pagina: int, limite: int) -> Dict[str, Any]:
    return {
        "items": items,
        "total": total,
        "pagina": pagina,
        "limite": limite,
        "total_paginas": ceil(total / limite) if total else 0,
    }
