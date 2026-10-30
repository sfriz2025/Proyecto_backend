from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from App.infrastructure.database import Base


class ProductoModel(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    platillo_id: Mapped[int] = mapped_column(
        ForeignKey("platillos.id"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    cantidad: Mapped[float] = mapped_column(Float, nullable=False)
    unidad: Mapped[str] = mapped_column(String(10), nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)

    platillo: Mapped["PlatilloModel"] = relationship(back_populates="productos")
