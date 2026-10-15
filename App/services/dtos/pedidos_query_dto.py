from dataclasses import dataclass
from typing import Optional

from App.domain.pedidos_domain import EstadoPedido


@dataclass
class PedidoQuery:
    estado: Optional[EstadoPedido] = None
    cuenta_id: Optional[int] = None
    ordenar_por: str = "id"
    direccion: str = "asc"
    pagina: int = 1
    limite: int = 10
