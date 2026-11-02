from dataclasses import dataclass


@dataclass
class ComparacionPlatilloDTO:
    """Resultado interno de comparar restaurante vs casa."""

    ahorro_dinero: float
    ahorro_tiempo_min: int
    es_conveniente: bool
