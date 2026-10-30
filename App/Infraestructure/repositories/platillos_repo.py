from typing import Optional

from App.domain.platillos_domain import Platillo
from App.Infraestructure.repositories.base_repo import InMemoryRepository


class PlatilloRepository(InMemoryRepository[Platillo]):
    def __init__(self) -> None:
        super().__init__()
        self.add(Platillo(0, "Lasaña", "pastas", 12000.0, 20, 15000.0, 60))
        self.add(Platillo(0, "Ensalada", "saludable", 8000.0, 10, 6500.0, 25))

    def buscar_por_nombre(self, nombre: str) -> Optional[Platillo]:
        buscado = nombre.strip().lower()
        return next((p for p in self._items.values() if p.nombre.lower() == buscado), None)


platillo_repo = PlatilloRepository()
