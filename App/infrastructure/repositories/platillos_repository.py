from sqlalchemy import func, select
from sqlalchemy.orm import Session


from App.domain.platillos_domain import Platillo
from App.infrastructure.mappers.platillo_mapper import (
    platillo_a_dominio,
    platillo_a_modelo,
)
from App.infrastructure.models import PlatilloModel


class PlatilloSQLRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, platillo_id: int) -> Platillo | None:
        consulta = select(PlatilloModel).where(
            PlatilloModel.id == platillo_id,
            PlatilloModel.activo.is_(True),
        )
        modelo = self.db.scalar(consulta)
        return platillo_a_dominio(modelo) if modelo is not None else None

    def get_all(self) -> list[Platillo]:
        consulta = select(PlatilloModel).where(PlatilloModel.activo.is_(True))
        modelos = self.db.scalars(consulta).all()
        return [platillo_a_dominio(modelo) for modelo in modelos]

    def add(self, platillo: Platillo) -> Platillo:
        modelo = platillo_a_modelo(platillo)
        self.db.add(modelo)

        try:
            self.db.commit()
            self.db.refresh(modelo)
        except Exception:
            self.db.rollback()
            raise

        return platillo_a_dominio(modelo)

    def update(self, platillo_id: int, platillo: Platillo) -> Platillo | None:
        consulta = select(PlatilloModel).where(
            PlatilloModel.id == platillo_id,
            PlatilloModel.activo.is_(True),
        )
        modelo = self.db.scalar(consulta)

        if modelo is None:
            return None

        modelo.nombre = platillo.nombre
        modelo.categoria = platillo.categoria
        modelo.precio_restaurante = platillo.precio_restaurante
        modelo.tiempo_restaurante_min = platillo.tiempo_restaurante_min
        modelo.costo_estimado_casa = platillo.costo_estimado_casa
        modelo.tiempo_casa_min = platillo.tiempo_casa_min

        try:
            self.db.commit()
            self.db.refresh(modelo)
        except Exception:
            self.db.rollback()
            raise

        return platillo_a_dominio(modelo)

    def buscar_por_nombre(self, nombre: str) -> Platillo | None:
        nombre_normalizado = nombre.strip().lower()
        consulta = select(PlatilloModel).where(
            func.lower(PlatilloModel.nombre) == nombre_normalizado,
            PlatilloModel.activo.is_(True),
        )
        modelo = self.db.scalar(consulta)
        return platillo_a_dominio(modelo) if modelo is not None else None

    def delete(self, platillo_id: int) -> bool:
        consulta = select(PlatilloModel).where(
            PlatilloModel.id == platillo_id,
            PlatilloModel.activo.is_(True),
        )
        modelo = self.db.scalar(consulta)

        if modelo is None:
            return False

        modelo.activo = False

        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        return True
