from typing import List, Optional

from App.domain.platillo import Platillo
from App.db.base_repository import IRepositoryInMemory


class PlatilloRepositoryInMemory(IRepositoryInMemory[Platillo]):
    def __init__(self):
        self._db_platillos = {
            1: Platillo(1, "Lasaña", "pastas", 12000.0, 20, 15000.0, 60),
            2: Platillo(2, "Ensalada", "saludable", 8000.0, 10, 6500.0, 25),
        }

    def get(self, id: int) -> Optional[Platillo]:
        return self._db_platillos.get(id)

    def get_all(self) -> List[Platillo]:
        return list(self._db_platillos.values())

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Platillo]:
        return self.get_all()[skip:skip + limit]

    def create(self, platillo: Platillo) -> Platillo:
        platillo_id = max(self._db_platillos.keys(), default=0) + 1
        platillo.id = platillo_id
        self._db_platillos[platillo_id] = platillo
        return platillo

    def update(self, id: int, platillo: Platillo) -> Optional[Platillo]:
        if id not in self._db_platillos:
            return None
        platillo.id = id
        self._db_platillos[id] = platillo
        return platillo

    def delete(self, id: int) -> bool:
        return self._db_platillos.pop(id, None) is not None
