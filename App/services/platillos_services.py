from dataclasses import asdict
from typing import Optional

from App.core.errors import ConflictError, NotFoundError
from App.core.pagination import construir_pagina, ordenar, paginar
from App.domain.platillos_domain import Platillo
from App.repositories.pedidos_repo import PedidoRepository
from App.repositories.platillos_repo import PlatilloRepository
from App.repositories.Productos_repo import ProductoRepository
from App.infrastructure.database import get_db_session
from App.infrastructure.repositories import PedidoRepository as SQLPedidoRepository, PlatilloRepository as SQLPlatilloRepository, ProductoRepository as SQLProductoRepository
from fastapi import Depends
from sqlalchemy.orm import Session
from App.schemas.platillos_shemas import PlatilloCreate, PlatilloResponse, PlatilloUpdate
from App.services.dtos.platillos_dto import ComparacionPlatilloDTO
from App.services.dtos.platillos_query_dto import PlatilloQuery


class PlatilloService:
    def __init__(
        self,
        repo: Optional[PlatilloRepository] = None,
        pedidos: Optional[PedidoRepository] = None,
        productos: Optional[ProductoRepository] = None,
    ):
        self.repo, self.pedidos, self.productos = repo, pedidos, productos

    # ---------- utilidades ----------
    def _obtener_o_404(self, platillo_id: int) -> Platillo:
        platillo = self.repo.get(platillo_id)
        if platillo is None:
            raise NotFoundError("No existe un platillo con el ID solicitado")
        return platillo

    def _a_response(self, p: Platillo) -> PlatilloResponse:
        comparacion = ComparacionPlatilloDTO(p.ahorro_dinero(), p.ahorro_tiempo_min(), p.es_conveniente())
        return PlatilloResponse(**asdict(p), **asdict(comparacion))

    def _validar_nombre_unico(self, nombre: str, ignorar_id: Optional[int] = None) -> None:
        existente = self.repo.buscar_por_nombre(nombre)
        if existente is not None and existente.id != ignorar_id:
            raise ConflictError(
                "Ya existe un platillo con ese nombre",
                [{"campo": "nombre", "mensaje": "El nombre ya está registrado"}],
            )

    # ---------- casos de uso ----------
    def listar(self, q: PlatilloQuery) -> dict:
        """Filtrar -> ordenar -> paginar (en ese orden)."""
        pagina, total = self.repo.list_page({"categoria": q.categoria}, q.ordenar_por, q.direccion, q.pagina, q.limite)
        return construir_pagina([self._a_response(p) for p in pagina], total, q.pagina, q.limite)

    def crear(self, datos: PlatilloCreate) -> PlatilloResponse:
        self._validar_nombre_unico(datos.nombre)
        platillo = self.repo.add(Platillo(id=0, **datos.model_dump()))
        return self._a_response(platillo)

    def obtener(self, platillo_id: int) -> PlatilloResponse:
        return self._a_response(self._obtener_o_404(platillo_id))

    def actualizar(self, platillo_id: int, datos: PlatilloUpdate) -> PlatilloResponse:
        actual = self._obtener_o_404(platillo_id)
        cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
        if "nombre" in cambios:
            self._validar_nombre_unico(cambios["nombre"], ignorar_id=platillo_id)
        actualizado = self.repo.update(platillo_id, Platillo(**{**asdict(actual), **cambios}))
        return self._a_response(actualizado)

    def eliminar(self, platillo_id: int) -> None:
        self._obtener_o_404(platillo_id)
        # Regla de negocio: no se elimina un platillo con pedidos activos.
        if self.pedidos.tiene_activos_de_platillo(platillo_id):
            raise ConflictError("No se puede eliminar un platillo con pedidos activos")
        self.productos.eliminar_por_platillo(platillo_id)
        self.repo.delete(platillo_id)


def get_platillo_service(session: Session = Depends(get_db_session)) -> PlatilloService:
    return PlatilloService(SQLPlatilloRepository(session), SQLPedidoRepository(session), SQLProductoRepository(session))
