from typing import List

from App.domain.productos_domain import Producto, Unidad
from App.Infraestructure.repositories.base_repo import InMemoryRepository


class ProductoRepository(InMemoryRepository[Producto]):
    def __init__(self) -> None:
        super().__init__()
        self.add(Producto(0, 1, "Pasta de lasaña", 500, Unidad.GRAMO, 3.0))
        self.add(Producto(0, 1, "Salsa de tomate", 400, Unidad.MILILITRO, 2.5))

    def obtener_por_platillo(self, platillo_id: int) -> List[Producto]:
        return [p for p in self._items.values() if p.platillo_id == platillo_id]

    def eliminar_por_platillo(self, platillo_id: int) -> None:
        for p in self.obtener_por_platillo(platillo_id):
            self._items.pop(p.id, None)


producto_repo = ProductoRepository()
