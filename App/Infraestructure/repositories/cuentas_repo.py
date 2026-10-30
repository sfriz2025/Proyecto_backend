from datetime import datetime
from typing import Optional

from App.domain.cuentas_domain import Cuenta
from App.Infraestructure.repositories.base_repo import InMemoryRepository


class CuentaRepository(InMemoryRepository[Cuenta]):
    def __init__(self) -> None:
        super().__init__()
        self.add(Cuenta(0, "Camila Rojas", "camila@correo.cl", 150000.0, datetime.now()))
        self.add(Cuenta(0, "Diego Soto", "diego@correo.cl", 80000.0, datetime.now()))

    def buscar_por_correo(self, correo: str) -> Optional[Cuenta]:
        buscado = correo.strip().lower()
        return next((c for c in self._items.values() if c.correo == buscado), None)


cuenta_repo = CuentaRepository()
