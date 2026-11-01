from sqlalchemy import func, select
from sqlalchemy.orm import Session

from App.domain.cuentas_domain import Cuenta
from App.infrastructure.mappers.cuenta_mapper import cuenta_a_dominio, cuenta_a_modelo
from App.infrastructure.models import CuentaModel


class CuentaSQLRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, cuenta_id: int) -> Cuenta | None:
        modelo = self.db.get(CuentaModel, cuenta_id)
        return cuenta_a_dominio(modelo) if modelo is not None else None

    def get_all(self) -> list[Cuenta]:
        modelos = self.db.scalars(select(CuentaModel)).all()
        return [cuenta_a_dominio(modelo) for modelo in modelos]

    def add(self, cuenta: Cuenta) -> Cuenta:
        modelo = cuenta_a_modelo(cuenta)
        self.db.add(modelo)
        try:
            self.db.commit()
            self.db.refresh(modelo)
        except Exception:
            self.db.rollback()
            raise
        return cuenta_a_dominio(modelo)

    def update(self, cuenta_id: int, cuenta: Cuenta) -> Cuenta | None:
        modelo = self.db.get(CuentaModel, cuenta_id)
        if modelo is None:
            return None

        modelo.nombre_titular = cuenta.nombre_titular
        modelo.correo = cuenta.correo
        modelo.presupuesto_mensual = cuenta.presupuesto_mensual
        modelo.fecha_creacion = cuenta.fecha_creacion
        try:
            self.db.commit()
            self.db.refresh(modelo)
        except Exception:
            self.db.rollback()
            raise
        return cuenta_a_dominio(modelo)

    def delete(self, cuenta_id: int) -> bool:
        modelo = self.db.get(CuentaModel, cuenta_id)
        if modelo is None:
            return False
        self.db.delete(modelo)
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        return True

    def buscar_por_correo(self, correo: str) -> Cuenta | None:
        normalizado = correo.strip().lower()
        modelo = self.db.scalar(
            select(CuentaModel).where(func.lower(CuentaModel.correo) == normalizado)
        )
        return cuenta_a_dominio(modelo) if modelo is not None else None

    def listar(
        self,
        nombre: str | None,
        ordenar_por: str,
        direccion: str,
        pagina: int,
        limite: int,
    ) -> tuple[list[Cuenta], int]:
        stmt = select(CuentaModel)
        count_stmt = select(func.count()).select_from(CuentaModel)
        if nombre:
            filtro = CuentaModel.nombre_titular.ilike(f"%{nombre.strip()}%")
            stmt = stmt.where(filtro)
            count_stmt = count_stmt.where(filtro)

        total = self.db.scalar(count_stmt) or 0
        columna = getattr(CuentaModel, ordenar_por)
        if ordenar_por == "nombre_titular":
            columna = func.lower(columna)
        stmt = stmt.order_by(columna.desc() if direccion == "desc" else columna.asc())
        stmt = stmt.offset((pagina - 1) * limite).limit(limite)
        modelos = self.db.scalars(stmt).all()
        return [cuenta_a_dominio(modelo) for modelo in modelos], total
