from fastapi import FastAPI

from App.core.errors import registrar_manejadores
from App.presentation.routers import Platillos, Producto, cuentas
from App.presentation.routers import pedidos

app = FastAPI(
    title="FoodCart API",
    description=(
        "API para registrar pedidos y gastos de comida y comparar si conviene comer en un "
        "restaurante o cocinar en casa. Almacenamiento en memoria."
    ),
    version="1.0.0",
)

registrar_manejadores(app)

app.include_router(Platillos.router)
app.include_router(Producto.router)
app.include_router(cuentas.router)
app.include_router(pedidos.router)
