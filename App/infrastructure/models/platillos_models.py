from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from App.infrastructure.database import Base


class PlatilloModel(Base):
    __tablename__ = "platillos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    precio_restaurante: Mapped[float] = mapped_column(Float, nullable=False)
    tiempo_restaurante_min: Mapped[int] = mapped_column(Integer, nullable=False)
    costo_estimado_casa: Mapped[float] = mapped_column(Float, nullable=False)
    tiempo_casa_min: Mapped[int] = mapped_column(Integer, nullable=False)

    productos: Mapped[list["ProductoModel"]] = relationship(
        back_populates="platillo"
    )
    pedidos: Mapped[list["PedidoModel"]] = relationship(back_populates="platillo")
