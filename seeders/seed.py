"""Carga idempotente de datos de ejemplo para FoodCart."""

from datetime import datetime

from sqlalchemy import select

from infrastructure.database import SessionLocal
from infrastructure.models import CuentaModel, PedidoModel, PlatilloModel, ProductoModel


def seed() -> None:
    """Crea dos registros por entidad sin duplicarlos al volver a ejecutar el script."""
    with SessionLocal.begin() as db:
        cuentas_demo = [
            {
                "nombre_titular": "Ana Demo",
                "correo": "ana.demo@foodcart.local",
                "presupuesto_mensual": 180000.0,
            },
            {
                "nombre_titular": "Luis Demo",
                "correo": "luis.demo@foodcart.local",
                "presupuesto_mensual": 160000.0,
            },
        ]
        cuentas: dict[str, CuentaModel] = {}
        for datos in cuentas_demo:
            cuenta = db.scalar(
                select(CuentaModel).where(CuentaModel.correo == datos["correo"])
            )
            if cuenta is None:
                cuenta = CuentaModel(**datos, fecha_creacion=datetime.now())
                db.add(cuenta)
                db.flush()
            cuentas[datos["correo"]] = cuenta

        platillos_demo = [
            {
                "nombre": "Hamburguesa Demo FoodCart",
                "categoria": "comida_rapida",
                "precio_restaurante": 6500.0,
                "tiempo_restaurante_min": 20,
                "costo_estimado_casa": 8200.0,
                "tiempo_casa_min": 45,
                "activo": True,
            },
            {
                "nombre": "Pasta Demo FoodCart",
                "categoria": "pastas",
                "precio_restaurante": 7200.0,
                "tiempo_restaurante_min": 25,
                "costo_estimado_casa": 5600.0,
                "tiempo_casa_min": 40,
                "activo": True,
            },
        ]
        platillos: dict[str, PlatilloModel] = {}
        for datos in platillos_demo:
            platillo = db.scalar(
                select(PlatilloModel).where(
                    PlatilloModel.nombre == datos["nombre"],
                    PlatilloModel.activo.is_(True),
                )
            )
            if platillo is None:
                platillo = PlatilloModel(**datos)
                db.add(platillo)
                db.flush()
            platillos[datos["nombre"]] = platillo

        productos_demo = [
            ("Hamburguesa Demo FoodCart", "Carne", 250.0, "g", 0.018),
            ("Hamburguesa Demo FoodCart", "Pan", 2.0, "unidad", 700.0),
            ("Pasta Demo FoodCart", "Pasta", 200.0, "g", 0.012),
            ("Pasta Demo FoodCart", "Salsa de tomate", 150.0, "g", 0.01),
        ]
        for nombre_platillo, nombre, cantidad, unidad, precio_unitario in productos_demo:
            platillo = platillos[nombre_platillo]
            producto = db.scalar(
                select(ProductoModel).where(
                    ProductoModel.platillo_id == platillo.id,
                    ProductoModel.nombre == nombre,
                )
            )
            if producto is None:
                db.add(
                    ProductoModel(
                        platillo_id=platillo.id,
                        nombre=nombre,
                        cantidad=cantidad,
                        unidad=unidad,
                        precio_unitario=precio_unitario,
                    )
                )

        pedidos_demo = [
            ("ana.demo@foodcart.local", "Hamburguesa Demo FoodCart", "restaurante", 1),
            ("luis.demo@foodcart.local", "Pasta Demo FoodCart", "casa", 2),
        ]
        for correo, nombre_platillo, modalidad, cantidad in pedidos_demo:
            cuenta = cuentas[correo]
            platillo = platillos[nombre_platillo]
            pedido = db.scalar(
                select(PedidoModel).where(
                    PedidoModel.cuenta_id == cuenta.id,
                    PedidoModel.platillo_id == platillo.id,
                )
            )
            if pedido is None:
                precio = (
                    platillo.precio_restaurante
                    if modalidad == "restaurante"
                    else platillo.costo_estimado_casa
                )
                db.add(
                    PedidoModel(
                        cuenta_id=cuenta.id,
                        platillo_id=platillo.id,
                        modalidad=modalidad,
                        cantidad=cantidad,
                        estado="pendiente",
                        fecha=datetime.now(),
                        total=round(precio * cantidad, 2),
                    )
                )

    print("Seeder ejecutado: datos de ejemplo listos (sin duplicar registros).")


if __name__ == "__main__":
    seed()
