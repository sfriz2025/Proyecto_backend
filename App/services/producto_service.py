# app/services/producto_service.py
from typing import List, Optional
from app.db.repositories.producto_repo import ProductoRepositoryInMemory
from app.domain.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate

# Inyectamos el repositorio
class ProductoService:
    def __init__(self, repo: ProductoRepositoryInMemory = ProductoRepositoryInMemory()):
        self.repo = repo

    def get_producto(self, producto_id: int) -> Optional[Producto]:
        return self.repo.get(producto_id)

    def get_productos(self, skip: int = 0, limit: int = 10) -> List[Producto]:
        # Aquí puedes agregar lógica de negocio (ej: filtrar por categoría)
        #antes de llamar al repositorio.
        return self.repo.get_multi(skip=skip, limit=limit)

    def create_producto(self, producto_in: ProductoCreate) -> Producto:
        # Convertimos el DTO a Entidad de Dominio
        producto_obj = Producto(
            id=0, # El repositorio generará el ID
            nombre=producto_in.nombre,
            precio=producto_in.precio,
            disponible=producto_in.disponible,
            categoria=producto_in.categoria
        )
        # Regla de negocio: No se puede crear un producto con precio negativo
        if producto_obj.precio <= 0:
            raise ValueError("El precio debe ser mayor a cero")
            
        return self.repo.create(producto_obj)