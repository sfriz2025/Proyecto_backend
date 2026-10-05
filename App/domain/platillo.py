class Platillo:
    """Entidad de dominio para un platillo del catálogo."""

    def __init__(
        self,
        id: int,
        nombre: str,
        categoria: str,
        precio_restaurante: float,
        tiempo_restaurante_min: int,
        costo_estimado_casa: float,
        tiempo_casa_min: int,
    ):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.precio_restaurante = precio_restaurante
        self.tiempo_restaurante_min = tiempo_restaurante_min
        self.costo_estimado_casa = costo_estimado_casa
        self.tiempo_casa_min = tiempo_casa_min
