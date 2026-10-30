from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from App.infrastructure.database import Base


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    cuenta_id: Mapped[int] = mapped_column(
        ForeignKey("cuentas.id"), nullable=False
    )
    platillo_id: Mapped[int] = mapped_column(
        ForeignKey("platillos.id"), nullable=False
    )
    modalidad: Mapped[str] = mapped_column(String(20), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)

    cuenta: Mapped["CuentaModel"] = relationship(back_populates="pedidos")
    platillo: Mapped["PlatilloModel"] = relationship(back_populates="pedidos")
