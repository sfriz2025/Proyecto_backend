# app/domain/producto.py
class Producto:
    def __init__(self, id: int, nombre: str, precio: float, disponible: bool, categoria: str):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.disponible = disponible
        self.categoria = categoria