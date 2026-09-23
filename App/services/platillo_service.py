# app/services/platillo_service.py
from typing import List, Optional
from App.schemas.platillo import PlatilloCreate, PlatilloResponse, PlatilloUpdate
from App.db.repositories.platillo_repo import PlatilloRepositoryInMemory


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

        platillo_creado = self.repo.create(datos)
        return self._enriquecer_platillo(platillo_creado)