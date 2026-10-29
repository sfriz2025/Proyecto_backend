from datetime import datetime

from sqlalchemy import select

from App.domain.pedidos_domain import EstadoPedido, Modalidad
from App.domain.productos_domain import Unidad
from App.infrastructure.database import SessionLocal
from App.infrastructure.models import CuentaORM, PedidoORM, PlatilloORM, ProductoORM


def seed():
    with SessionLocal() as session:
        if session.scalar(select(CuentaORM.id).limit(1)):
            print("Ya existen datos; no se modificó la base.")
            return
        cuentas = [
            CuentaORM(nombre_titular="Camila Rojas", correo="camila@correo.cl", presupuesto_mensual=150000, fecha_creacion=datetime.now()),
            CuentaORM(nombre_titular="Diego Soto", correo="diego@correo.cl", presupuesto_mensual=80000, fecha_creacion=datetime.now()),
        ]
        platillos = [
            PlatilloORM(nombre="Lasaña", categoria="pastas", precio_restaurante=12000, tiempo_restaurante_min=20, costo_estimado_casa=15000, tiempo_casa_min=60),
            PlatilloORM(nombre="Ensalada", categoria="saludable", precio_restaurante=8000, tiempo_restaurante_min=10, costo_estimado_casa=6500, tiempo_casa_min=25),
        ]
        session.add_all(cuentas + platillos)
        session.flush()
        session.add_all([
            ProductoORM(platillo_id=platillos[0].id, nombre="Pasta de lasaña", cantidad=500, unidad=Unidad.GRAMO, precio_unitario=3),
            ProductoORM(platillo_id=platillos[1].id, nombre="Tomate", cantidad=2, unidad=Unidad.UNIDAD, precio_unitario=800),
        ])
        session.add_all([
            PedidoORM(cuenta_id=cuentas[0].id, platillo_id=platillos[0].id, modalidad=Modalidad.RESTAURANTE, cantidad=1, estado=EstadoPedido.ENTREGADO, fecha=datetime.now(), total=12000),
            PedidoORM(cuenta_id=cuentas[1].id, platillo_id=platillos[1].id, modalidad=Modalidad.CASA, cantidad=1, estado=EstadoPedido.PENDIENTE, fecha=datetime.now(), total=6500),
        ])
        session.commit()
        print("Seed aplicado: 2 cuentas, 2 platillos, 2 productos y 2 pedidos.")


if __name__ == "__main__":
    seed()
