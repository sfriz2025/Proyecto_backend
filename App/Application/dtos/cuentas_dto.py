from dataclasses import dataclass


@dataclass
class ResumenGastoDTO:
    cuenta_id: int
    presupuesto_mensual: float
    gasto_mes: float
    disponible: float
