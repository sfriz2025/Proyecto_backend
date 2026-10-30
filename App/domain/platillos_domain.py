from dataclasses import dataclass


@dataclass
class Platillo:
    """Entidad de dominio para un platillo del catálogo."""

    id: int
    nombre: str
    categoria: str
    precio_restaurante: float
    tiempo_restaurante_min: int
    costo_estimado_casa: float
    tiempo_casa_min: int

    # ---- Regla de negocio: ¿conviene comprarlo en el restaurante? ----
    def ahorro_dinero(self) -> float:
        """Positivo si el restaurante es más barato que cocinar en casa."""
        return round(self.costo_estimado_casa - self.precio_restaurante, 2)

    def ahorro_tiempo_min(self) -> int:
        """Positivo si el restaurante es más rápido que cocinar en casa."""
        return self.tiempo_casa_min - self.tiempo_restaurante_min

    def es_conveniente(self) -> bool:
        """Conviene el restaurante si ahorra dinero y no tarda más que en casa."""
        return self.ahorro_dinero() > 0 and self.ahorro_tiempo_min() >= 0
