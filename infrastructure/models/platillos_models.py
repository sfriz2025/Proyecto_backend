from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure.models.pedidos_models import PedidoModel
    from infrastructure.models.productos_models import ProductoModel
from sqlalchemy import Boolean, Float, Index, Integer, String, text, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database import Base


class PlatilloModel(Base):
    __tablename__ = "platillos"
    __table_args__ = (
        Index(
            "uq_platillos_nombre_activo",
            "nombre",
            unique=True,
            postgresql_where=text("activo IS TRUE"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    precio_restaurante: Mapped[float] = mapped_column(Float, nullable=False)
    tiempo_restaurante_min: Mapped[int] = mapped_column(Integer, nullable=False)
    costo_estimado_casa: Mapped[float] = mapped_column(Float, nullable=False)
    tiempo_casa_min: Mapped[int] = mapped_column(Integer, nullable=False)
    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=true(),
    )

    productos: Mapped[list["ProductoModel"]] = relationship(
        back_populates="platillo"
    )
    pedidos: Mapped[list["PedidoModel"]] = relationship(back_populates="platillo")
