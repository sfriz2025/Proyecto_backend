from typing import Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    """Almacenamiento en memoria con ID autoincremental. Las entidades deben tener el atributo `id`."""

    def __init__(self) -> None:
        self._items: Dict[int, T] = {}
        self._siguiente_id = 1

    def get(self, id: int) -> Optional[T]:
        return self._items.get(id)

    def get_all(self) -> List[T]:
        return list(self._items.values())

    def add(self, entidad: T) -> T:
        entidad.id = self._siguiente_id  # type: ignore[attr-defined]
        self._items[entidad.id] = entidad  # type: ignore[attr-defined]
        self._siguiente_id += 1
        return entidad

    def update(self, id: int, entidad: T) -> T:
        entidad.id = id  # type: ignore[attr-defined]
        self._items[id] = entidad
        return entidad

    def delete(self, id: int) -> bool:
        return self._items.pop(id, None) is not None
