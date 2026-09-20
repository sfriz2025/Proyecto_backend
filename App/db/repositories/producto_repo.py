# app/db/repositories/producto_repo.py
from typing import List, Optional
from app.domain.producto import Producto
from app.db.base_repository import IRepositoryInMemory

# Simulación de la base de datos en memoria (un diccionario)
# El encargado de Dominio y Datos debe poblar esto.
_db_productos = {
    1: Producto(id=1, nombre="Hamburguesa Clásica", precio=8500.0, disponible=True, categoria="hamburguesas"),
    2: Producto(id=2, nombre="Papas Fritas", precio=3500.0, disponible=True, categoria="acompañamientos"),
}

class ProductoRepositoryInMemory(IRepositoryInMemory[Producto]):
    def get(self, id: int) -> Optional[Producto]:
        return _db_productos.get(id)

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        return list(_db_productos.values())[skip: skip + limit]

    def create(self, producto: Producto) -> Producto:
        # Lógica para generar el siguiente ID
        producto_id = max(_db_productos.keys()) + 1 if _db_productos else 1
        producto.id = producto_id
        _db_productos[producto_id] = producto
        return producto

    # ... y así con el resto de métodos ...