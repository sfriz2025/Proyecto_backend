from fastapi import Depends
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from infrastructure.repositories.platillos_repository import PlatilloSQLRepository
from infrastructure.repositories.productos_repository import ProductoSQLRepository
from dataclasses import asdict
from typing import Optional
from core.errors import NotFoundError
from core.pagination import construir_pagina, ordenar, paginar
from domain.productos_domain import Producto
from presentation.schemas.producto_shemas import ProductoCreate, ProductoResponse
from application.services.dtos.productos_query_dto import ProductoQuery
#Los imports traen las clases y funciones necesarias para interactuar con la base de datos,
#manejar errores, paginación y definir los esquemas de datos para los productos.
#-----------------------------


class ProductoService:
    def __init__(
        self,
        repo,
        platillos,
    ):
        self.repo = repo
        self.platillos = platillos

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


def get_producto_service(db: Session = Depends(get_db)) -> ProductoService:
    return ProductoService(
        repo=ProductoSQLRepository(db),
        platillos=PlatilloSQLRepository(db),
    )

#-----------------------------
# ANOTACIONES:
# 1. La clase ProductoService es un servicio que maneja la lógica de negocio relacionada
#    con los productos. Proporciona métodos para listar, crear y eliminar productos.
