# app/db/repositories/producto_repo.py
from typing import List, Optional
from App.domain.platillo import Platillo
from App.db.base_repository import IRepositoryInMemory


class PlatilloRepositoryInMemory(IRepositoryInMemory[Platillo]):
    def __init__(self):
        self._db_platillos = {
            1: Platillo(id=1, nombre="Lasaña", precio_restaurante=12000.0, categoria="pastas"),
            2: Platillo(id=2, nombre="Ensalada", precio_restaurante=8000.0, categoria="saludable"),
        }

    def get(self, id: int) -> Optional[Platillo]:
        return self._db_platillos.get(id)

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Platillo]:
        return list(self._db_platillos.values())[skip: skip + limit]

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

    def delete(self, id: int) -> None:
        if id in self._db_platillos:
            del self._db_platillos[id]