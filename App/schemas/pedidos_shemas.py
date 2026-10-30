from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from App.domain.pedidos_domain import EstadoPedido, Modalidad


class PedidoCreate(BaseModel):
    cuenta_id: int = Field(..., gt=0, examples=[1])
    platillo_id: int = Field(..., gt=0, examples=[1])
    modalidad: Modalidad = Field(..., examples=["restaurante"])
    cantidad: int = Field(..., ge=1, le=20, examples=[2])


class PedidoEstadoUpdate(BaseModel):
    estado: EstadoPedido = Field(..., examples=["confirmado"])


class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cuenta_id: int
    platillo_id: int
    modalidad: Modalidad
    cantidad: int
    estado: EstadoPedido
    fecha: datetime
    total: float
