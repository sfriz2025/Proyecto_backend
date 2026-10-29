from datetime import datetime

from sqlalchemy import DateTime, Enum as SAEnum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from App.domain.pedidos_domain import EstadoPedido, Modalidad
from App.domain.productos_domain import Unidad
from App.infrastructure.database import Base


class CuentaORM(Base):
    __tablename__ = "cuentas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre_titular: Mapped[str] = mapped_column(String(60), nullable=False)
    correo: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    presupuesto_mensual: Mapped[float] = mapped_column(Float, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pedidos: Mapped[list["PedidoORM"]] = relationship(back_populates="cuenta", cascade="all, delete-orphan")


class PlatilloORM(Base):
    __tablename__ = "platillos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    categoria: Mapped[str] = mapped_column(String(30), index=True, nullable=False)
    precio_restaurante: Mapped[float] = mapped_column(Float, nullable=False)
    tiempo_restaurante_min: Mapped[int] = mapped_column(Integer, nullable=False)
    costo_estimado_casa: Mapped[float] = mapped_column(Float, nullable=False)
    tiempo_casa_min: Mapped[int] = mapped_column(Integer, nullable=False)
    productos: Mapped[list["ProductoORM"]] = relationship(back_populates="platillo", cascade="all, delete-orphan")
    pedidos: Mapped[list["PedidoORM"]] = relationship(back_populates="platillo")


class ProductoORM(Base):
    __tablename__ = "productos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    platillo_id: Mapped[int] = mapped_column(ForeignKey("platillos.id", ondelete="CASCADE"), index=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    cantidad: Mapped[float] = mapped_column(Float, nullable=False)
    unidad: Mapped[Unidad] = mapped_column(SAEnum(Unidad, native_enum=False), nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Float, nullable=False)
    platillo: Mapped[PlatilloORM] = relationship(back_populates="productos")


class PedidoORM(Base):
    __tablename__ = "pedidos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cuenta_id: Mapped[int] = mapped_column(ForeignKey("cuentas.id", ondelete="CASCADE"), index=True)
    platillo_id: Mapped[int] = mapped_column(ForeignKey("platillos.id"), index=True)
    modalidad: Mapped[Modalidad] = mapped_column(SAEnum(Modalidad, native_enum=False), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[EstadoPedido] = mapped_column(SAEnum(EstadoPedido, native_enum=False), index=True, nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    cuenta: Mapped[CuentaORM] = relationship(back_populates="pedidos")
    platillo: Mapped[PlatilloORM] = relationship(back_populates="pedidos")
