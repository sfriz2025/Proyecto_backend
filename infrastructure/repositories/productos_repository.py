from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.productos_domain import Producto
from infrastructure.mappers.producto_mapper import (
    producto_a_dominio,
    producto_a_modelo,
)
from infrastructure.models import ProductoModel

#Estas importaciones traen las clases necesarias para interactuar con la base de datos
#  y mapear entre el modelo de dominio Producto y el modelo de base de datos ProductoModel.

class ProductoSQLRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, producto_id: int) -> Producto | None:
        consulta = select(ProductoModel).where(
            ProductoModel.id == producto_id
        )
        modelo = self.db.scalar(consulta)

        if modelo is None:
            return None

        return producto_a_dominio(modelo)


    def get_all(self) -> list[Producto]:
        consulta = select(ProductoModel)
        modelos = self.db.scalars(consulta).all()

        return [producto_a_dominio(modelo) for modelo in modelos]

    def obtener_por_platillo(self, platillo_id: int) -> list[Producto]:
        consulta = select(ProductoModel).where(
            ProductoModel.platillo_id == platillo_id
        )
        modelos = self.db.scalars(consulta).all()

        return [producto_a_dominio(modelo) for modelo in modelos]

    def add(self, producto: Producto) -> Producto:
        modelo = producto_a_modelo(producto)
        self.db.add(modelo)

        try:
            self.db.commit()
            self.db.refresh(modelo)
        except Exception:
            self.db.rollback()
            raise

        return producto_a_dominio(modelo)

    def eliminar_por_platillo(self, platillo_id: int) -> None:
        productos = self.db.scalars(
            select(ProductoModel).where(
                ProductoModel.platillo_id == platillo_id
            )
        ).all()

        try:
            for producto in productos:
                self.db.delete(producto)

            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def delete(self, producto_id: int) -> bool:
        modelo = self.db.get(ProductoModel, producto_id)

        if modelo is None:
            return False

        try:
            self.db.delete(modelo)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        return True
#----------------------------------------
# Anotaciones:
#----------------------------------------

#1. Esta clase ProductoSQLRepository es un repositorio que proporciona métodos para interactuar con la base de datos
#y realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en los productos.
#2. Las funciones get, get_all, get_by_platillo, add y delete_by_platillo permiten obtener productos por su ID,
#obtener todos los productos, obtener productos asociados a un platillo específico,
# agregar un nuevo producto y eliminar productos asociados a un platillo, respectivamente.
