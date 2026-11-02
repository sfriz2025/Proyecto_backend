from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PlatilloBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, examples=["Hamburguesa Casera"])
    categoria: str = Field(..., min_length=3, max_length=30, examples=["comida_rapida"])

    # Datos del restaurante
    precio_restaurante: float = Field(..., gt=0, examples=[8500.0])
    tiempo_restaurante_min: int = Field(..., gt=0, examples=[15])

    # Datos de preparación en casa (para la comparación)
    costo_estimado_casa: float = Field(..., gt=0, examples=[11000.0])
    tiempo_casa_min: int = Field(..., gt=0, examples=[45])


class PlatilloCreate(PlatilloBase):
    pass


class PlatilloUpdate(BaseModel):
    """PATCH: todos los campos son opcionales."""

    nombre: Optional[str] = Field(None, min_length=3, max_length=50)
    categoria: Optional[str] = Field(None, min_length=3, max_length=30)
    precio_restaurante: Optional[float] = Field(None, gt=0)
    tiempo_restaurante_min: Optional[int] = Field(None, gt=0)
    costo_estimado_casa: Optional[float] = Field(None, gt=0)
    tiempo_casa_min: Optional[int] = Field(None, gt=0)


class PlatilloResponse(PlatilloBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # Campos calculados por la lógica de negocio
    ahorro_dinero: float
    ahorro_tiempo_min: int
    es_conveniente: bool
