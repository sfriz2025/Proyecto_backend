from pydantic import BaseModel, ConfigDict, Field

from App.domain.productos_domain import Unidad


class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50, examples=["Queso rallado"])
    cantidad: float = Field(..., gt=0, examples=[200])
    unidad: Unidad = Field(..., examples=["g"])
    precio_unitario: float = Field(..., gt=0, examples=[4.5])


class ProductoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    platillo_id: int
    nombre: str
    cantidad: float
    unidad: Unidad
    precio_unitario: float
    costo_total: float
