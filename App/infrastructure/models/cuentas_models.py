from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from App.infrastructure.database import Base


class CuentaModel(Base):
    __tablename__ = "cuentas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_titular: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    presupuesto_mensual: Mapped[float] = mapped_column(Float, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    pedidos: Mapped[list["PedidoModel"]] = relationship(back_populates="cuenta")
