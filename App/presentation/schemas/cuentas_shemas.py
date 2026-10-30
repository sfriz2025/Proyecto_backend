from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

CORREO_PATRON = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class CuentaCreate(BaseModel):
    nombre_titular: str = Field(..., min_length=3, max_length=60, examples=["Camila Rojas"])
    correo: str = Field(..., pattern=CORREO_PATRON, examples=["camila@correo.cl"])
    presupuesto_mensual: float = Field(..., gt=0, examples=[150000.0])


class CuentaUpdate(BaseModel):
    """PATCH: todos los campos son opcionales."""

    nombre_titular: Optional[str] = Field(None, min_length=3, max_length=60)
    correo: Optional[str] = Field(None, pattern=CORREO_PATRON)
    presupuesto_mensual: Optional[float] = Field(None, gt=0)


class CuentaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre_titular: str
    correo: str
    presupuesto_mensual: float
    fecha_creacion: datetime


class ResumenCuentaResponse(BaseModel):
    cuenta_id: int
    presupuesto_mensual: float
    gasto_mes: float
    disponible: float
