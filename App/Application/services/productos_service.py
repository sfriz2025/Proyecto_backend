from dataclasses import asdict
from typing import Optional

from App.core.errors import NotFoundError
from App.core.pagination import construir_pagina, ordenar, paginar
from App.domain.productos_domain import Producto
from App.Infraestructure.repositories.platillos_repo import PlatilloRepository, platillo_repo
from App.Infraestructure.repositories.Productos_repo import ProductoRepository, producto_repo
from App.presentation.schemas.producto_shemas import ProductoCreate, ProductoResponse
from App.Application.dtos.productos_query_dto import ProductoQuery


class ProductoService:
    def __init__(
        self,
        repo: Optional[ProductoRepository] = None,
        platillos: Optional[PlatilloRepository] = None,
    ):
        self.repo = repo if repo is not None else producto_repo
        self.platillos = platillos if platillos is not None else platillo_repo

    def _a_response(self, p: Producto) -> ProductoResponse:
        return ProductoResponse(**asdict(p), costo_total=p.costo_total())

    def _validar_platillo(self, platillo_id: int) -> None:
        if self.platillos.get(platillo_id) is None:
            raise NotFoundError("No existe un platillo con el ID solicitado")

    def listar_por_platillo(self, platillo_id: int, q: ProductoQuery) -> dict:
        self._validar_platillo(platillo_id)
        productos = self.repo.obtener_por_platillo(platillo_id)
        if q.unidad is not None:
            productos = [p for p in productos if p.unidad == q.unidad]
        productos = ordenar(productos, q.ordenar_por, q.direccion)
        total = len(productos)
        pagina = paginar(productos, q.pagina, q.limite)
        return construir_pagina([self._a_response(p) for p in pagina], total, q.pagina, q.limite)

    def crear(self, platillo_id: int, datos: ProductoCreate) -> ProductoResponse:
        self._validar_platillo(platillo_id)
        producto = self.repo.add(Producto(id=0, platillo_id=platillo_id, **datos.model_dump()))
        return self._a_response(producto)

    def eliminar(self, producto_id: int) -> None:
        if not self.repo.delete(producto_id):
            raise NotFoundError("No existe un producto con el ID solicitado")


def get_producto_service() -> ProductoService:
    return ProductoService()
