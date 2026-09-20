# app/db/base_repository.py
from typing import TypeVar, Generic, List, Optional
from app.domain.base import EntidadBase  # Si usas una base

# 'T' es el tipo de la entidad de dominio (ej: Producto, Pedido)
T = TypeVar("T")

class IRepositoryInMemory(Generic[T]):
    """Interfaz abstracta para repositorios en memoria."""
    
    def get(self, id: int) -> Optional[T]:
        """Obtiene una entidad por ID."""
        raise NotImplementedError

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Obtiene múltiples entidades con paginación."""
        raise NotImplementedError

    def create(self, entity: T) -> T:
        """Crea una nueva entidad."""
        raise NotImplementedError

    def update(self, id: int, entity: T) -> Optional[T]:
        """Actualiza una entidad existente."""
        raise NotImplementedError

    def delete(self, id: int) -> bool:
        """Elimina una entidad por ID."""
        raise NotImplementedError