from App.domain.platillos_domain import Platillo
from App.infrastructure.models import PlatilloModel

def platillo_a_dominio(modelo: PlatilloModel) -> Platillo:
    return Platillo(
        id=modelo.id,
        nombre=modelo.nombre,
        categoria=modelo.categoria,
        precio_restaurante=modelo.precio_restaurante,
        tiempo_restaurante_min=modelo.tiempo_restaurante_min,
        costo_estimado_casa=modelo.costo_estimado_casa,
        tiempo_casa_min=modelo.tiempo_casa_min,
    )



def platillo_a_modelo(platillo: Platillo) -> PlatilloModel:
    return PlatilloModel(
        id=platillo.id if platillo.id > 0 else None,
        nombre=platillo.nombre,
        categoria=platillo.categoria,
        precio_restaurante=platillo.precio_restaurante,
        tiempo_restaurante_min=platillo.tiempo_restaurante_min,
        costo_estimado_casa=platillo.costo_estimado_casa,
        tiempo_casa_min=platillo.tiempo_casa_min
    )