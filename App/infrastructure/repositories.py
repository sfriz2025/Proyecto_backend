from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from App.domain.cuentas_domain import Cuenta
from App.domain.pedidos_domain import EstadoPedido, Pedido
from App.domain.platillos_domain import Platillo
from App.domain.productos_domain import Producto
from App.infrastructure.mappers import to_domain
from App.infrastructure.models.orm import CuentaORM, PedidoORM, PlatilloORM, ProductoORM


class SQLRepository:
    model = None
    domain = None

    def __init__(self, session: Session):
        self.session = session

    def get(self, ident):
        row = self.session.get(self.model, ident)
        return to_domain(row, self.domain) if row else None

    def get_all(self):
        return [to_domain(row, self.domain) for row in self.session.scalars(select(self.model))]

    def add(self, value):
        values = vars(value).copy()
        values.pop("id", None)
        row = self.model(**values)
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return to_domain(row, self.domain)

    def update(self, ident, value):
        row = self.session.get(self.model, ident)
        for key, val in vars(value).items():
            setattr(row, key, val)
        self.session.commit()
        self.session.refresh(row)
        return to_domain(row, self.domain)

    def delete(self, ident):
        row = self.session.get(self.model, ident)
        if row is None:
            return False
        self.session.delete(row)
        self.session.commit()
        return True

    def list_page(self, filters, sort, direction, page, limit, contains=()):
        query = select(self.model)
        for field, value in filters.items():
            if value is not None and value != "":
                column = getattr(self.model, field)
                query = query.where(column.ilike(f"%{value}%") if field in contains else column == value)
        total = self.session.scalar(select(func.count()).select_from(query.subquery())) or 0
        column = getattr(self.model, sort)
        query = query.order_by(column.desc() if direction == "desc" else column.asc())
        rows = self.session.scalars(query.offset((page - 1) * limit).limit(limit))
        return [to_domain(row, self.domain) for row in rows], total


class CuentaRepository(SQLRepository):
    model, domain = CuentaORM, Cuenta

    def buscar_por_correo(self, correo):
        row = self.session.scalar(select(CuentaORM).where(func.lower(CuentaORM.correo) == correo.lower()))
        return to_domain(row, Cuenta) if row else None


class PlatilloRepository(SQLRepository):
    model, domain = PlatilloORM, Platillo

    def buscar_por_nombre(self, nombre):
        row = self.session.scalar(select(PlatilloORM).where(func.lower(PlatilloORM.nombre) == nombre.strip().lower()))
        return to_domain(row, Platillo) if row else None


class ProductoRepository(SQLRepository):
    model, domain = ProductoORM, Producto

    def obtener_por_platillo(self, platillo_id):
        return [to_domain(row, Producto) for row in self.session.scalars(select(ProductoORM).where(ProductoORM.platillo_id == platillo_id))]

    def eliminar_por_platillo(self, platillo_id):
        self.session.query(ProductoORM).filter_by(platillo_id=platillo_id).delete(synchronize_session=False)
        self.session.commit()


class PedidoRepository(SQLRepository):
    model, domain = PedidoORM, Pedido

    def _exists_active(self, field, ident):
        return self.session.scalar(select(PedidoORM.id).where(getattr(PedidoORM, field) == ident, PedidoORM.estado.in_([EstadoPedido.PENDIENTE, EstadoPedido.CONFIRMADO])).limit(1)) is not None

    def tiene_activos_de_platillo(self, ident):
        return self._exists_active("platillo_id", ident)

    def tiene_activos_de_cuenta(self, ident):
        return self._exists_active("cuenta_id", ident)

    def eliminar_por_cuenta(self, ident):
        self.session.query(PedidoORM).filter_by(cuenta_id=ident).delete(synchronize_session=False)
        self.session.commit()

    def gasto_del_mes(self, cuenta_id, anio, mes):
        inicio = datetime(anio, mes, 1)
        fin = datetime(anio + (mes == 12), 1 if mes == 12 else mes + 1, 1)
        total = self.session.scalar(select(func.coalesce(func.sum(PedidoORM.total), 0)).where(PedidoORM.cuenta_id == cuenta_id, PedidoORM.estado != EstadoPedido.CANCELADO, PedidoORM.fecha >= inicio, PedidoORM.fecha < fin))
        return round(float(total or 0), 2)
