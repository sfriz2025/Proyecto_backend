from App.domain.productos_domain import Producto, Unidad
from App.infrastructure.models import ProductoModel

#Estas importaciones traen las clases necesarias para mapear
#entre el modelo de dominio Producto y el modelo de base de datos ProductoModel.

def producto_a_dominio(modelo: ProductoModel) -> Producto:
    return Producto(
        id=modelo.id,
        platillo_id=modelo.platillo_id,
        nombre=modelo.nombre,
        cantidad=modelo.cantidad,
        unidad=Unidad(modelo.unidad),
        precio_unitario=modelo.precio_unitario,
    )
#Esta función toma un objeto ProductoModel (que representa un producto en la base de datos)
#y lo convierte en un objeto Producto (que representa un producto en el dominio de la aplicación).

def producto_a_modelo(producto: Producto) -> ProductoModel:
    return ProductoModel(
        id=producto.id if producto.id > 0 else None,
        platillo_id=producto.platillo_id,
        nombre=producto.nombre,
        cantidad=producto.cantidad,
        unidad=producto.unidad.value,
        precio_unitario=producto.precio_unitario,
    )
#Esta función toma un objeto Producto (que representa un producto en el dominio de la aplicación)
#y lo convierte en un objeto ProductoModel (que representa un producto en la base de datos).


#-----------------------------------------------------------------------------------
#Este archivo contiene funciones para mapear entre el modelo de dominio Producto y
#el modelo de base de datos ProductoModel.
#Lo que hace mapper es convertir un objeto de un tipo a otro,
#en este caso de ProductoModel a Producto y viceversa.
