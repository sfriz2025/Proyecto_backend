# app/services/platillo_service.py
from typing import List, Optional
from App.schemas.platillo import PlatilloCreate, PlatilloResponse, PlatilloUpdate
from App.db.repositories.platillo_repo import PlatilloRepositoryInMemory
from App.domain.platillo import Platillo


class PlatilloService:
    def __init__(self, repo: Optional[PlatilloRepositoryInMemory] = None):
        self.repo = repo if repo is not None else PlatilloRepositoryInMemory()

    def _enriquecer_platillo(self, platillo_db) -> PlatilloResponse:
        """Regla de Negocio: Calcula ahorros y si es conveniente comer en el local."""
        ahorro_dinero = platillo_db.costo_estimado_casa - platillo_db.precio_restaurante
        ahorro_tiempo = platillo_db.tiempo_casa_min - platillo_db.tiempo_restaurante_min

        es_conveniente = ahorro_dinero > 0 or ahorro_tiempo > 0

        return PlatilloResponse(
            id=platillo_db.id,
            nombre=platillo_db.nombre,
            categoria=platillo_db.categoria,
            precio_restaurante=platillo_db.precio_restaurante,
            tiempo_restaurante_min=platillo_db.tiempo_restaurante_min,
            costo_estimado_casa=platillo_db.costo_estimado_casa,
            tiempo_casa_min=platillo_db.tiempo_casa_min,
            ahorro_dinero=ahorro_dinero,
            ahorro_tiempo_min=ahorro_tiempo,
            es_conveniente=es_conveniente
        )

    def obtener_platillos(
        self,
        categoria: Optional[str] = None,
        ordenar_por: Optional[str] = None,
        pagina: int = 1,
        limite: int = 10
    ) -> List[PlatilloResponse]:
        """Aplica Filtrado -> Ordenamiento -> Paginación (Requisito Obligatorio)"""
        platillos = self.repo.get_all()

        if categoria:
            platillos = [p for p in platillos if p.categoria.lower() == categoria.lower()]

        if ordenar_por == "precio":
            platillos.sort(key=lambda x: x.precio_restaurante)
        elif ordenar_por == "ahorro_tiempo":
            platillos.sort(key=lambda x: (x.tiempo_casa_min - x.tiempo_restaurante_min), reverse=True)

        inicio = (pagina - 1) * limite
        fin = inicio + limite
        platillos_paginados = platillos[inicio:fin]

        return [self._enriquecer_platillo(p) for p in platillos_paginados]

    def crear_platillo(self, datos: PlatilloCreate) -> PlatilloResponse:
        if datos.precio_restaurante <= 0:
            raise ValueError("El precio del restaurante debe ser mayor a 0")

        platillo_creado = self.repo.create(Platillo(id=0, **datos.model_dump()))
        return self._enriquecer_platillo(platillo_creado)

    def obtener_platillo(self, platillo_id: int) -> Optional[PlatilloResponse]:
        platillo = self.repo.get(platillo_id)
        return self._enriquecer_platillo(platillo) if platillo else None

    def actualizar_platillo(
        self, platillo_id: int, datos: PlatilloUpdate
    ) -> Optional[PlatilloResponse]:
        actual = self.repo.get(platillo_id)
        if actual is None:
            return None

        valores = {
            "nombre": actual.nombre,
            "categoria": actual.categoria,
            "precio_restaurante": actual.precio_restaurante,
            "tiempo_restaurante_min": actual.tiempo_restaurante_min,
            "costo_estimado_casa": actual.costo_estimado_casa,
            "tiempo_casa_min": actual.tiempo_casa_min,
        }
        valores.update(datos.model_dump(exclude_unset=True, exclude_none=True))
        actualizado = self.repo.update(platillo_id, Platillo(id=platillo_id, **valores))
        return self._enriquecer_platillo(actualizado) if actualizado else None

    def eliminar_platillo(self, platillo_id: int) -> bool:
        return self.repo.delete(platillo_id)
