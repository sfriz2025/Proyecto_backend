# app/schemas/platillo.py
from pydantic import BaseModel, Field
from typing import Optional

class PlatilloBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, example="Hamburguesa Casera")
    categoria: str = Field(..., example="comida_rapida")
    
    # Datos del Restaurante
    precio_restaurante: float = Field(..., gt=0, example=8500.0)
    tiempo_restaurante_min: int = Field(..., gt=0, example=15)
    
    # Datos de Preparación en Casa (para la comparación)
    costo_estimado_casa: float = Field(..., gt=0, example=11000.0)
    tiempo_casa_min: int = Field(..., gt=0, example=45)

class PlatilloCreate(PlatilloBase):
    pass

class PlatilloUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    precio_restaurante: Optional[float] = None
    tiempo_restaurante_min: Optional[int] = None
    costo_estimado_casa: Optional[float] = None
    tiempo_casa_min: Optional[int] = None

class PlatilloResponse(PlatilloBase):
    id: int
    # Campos calculados por la lógica de negocio
    ahorro_dinero: float
    ahorro_tiempo_min: int
    es_conveniente: bool

    class Config:
        orm_mode = True