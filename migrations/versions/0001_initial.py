"""Initial relational schema."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("cuentas", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("nombre_titular", sa.String(60), nullable=False), sa.Column("correo", sa.String(254), nullable=False), sa.Column("presupuesto_mensual", sa.Float(), nullable=False), sa.Column("fecha_creacion", sa.DateTime(), nullable=False), sa.UniqueConstraint("correo"))
    op.create_table("platillos", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("nombre", sa.String(50), nullable=False), sa.Column("categoria", sa.String(30), nullable=False), sa.Column("precio_restaurante", sa.Float(), nullable=False), sa.Column("tiempo_restaurante_min", sa.Integer(), nullable=False), sa.Column("costo_estimado_casa", sa.Float(), nullable=False), sa.Column("tiempo_casa_min", sa.Integer(), nullable=False), sa.UniqueConstraint("nombre"))
    op.create_index("ix_platillos_categoria", "platillos", ["categoria"])
    op.create_table("productos", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("platillo_id", sa.Integer(), sa.ForeignKey("platillos.id", ondelete="CASCADE"), nullable=False), sa.Column("nombre", sa.String(50), nullable=False), sa.Column("cantidad", sa.Float(), nullable=False), sa.Column("unidad", sa.String(9), nullable=False), sa.Column("precio_unitario", sa.Float(), nullable=False))
    op.create_index("ix_productos_platillo_id", "productos", ["platillo_id"])
    op.create_table("pedidos", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("cuenta_id", sa.Integer(), sa.ForeignKey("cuentas.id", ondelete="CASCADE"), nullable=False), sa.Column("platillo_id", sa.Integer(), sa.ForeignKey("platillos.id"), nullable=False), sa.Column("modalidad", sa.String(11), nullable=False), sa.Column("cantidad", sa.Integer(), nullable=False), sa.Column("estado", sa.String(10), nullable=False), sa.Column("fecha", sa.DateTime(), nullable=False), sa.Column("total", sa.Float(), nullable=False))
    for field in ("cuenta_id", "platillo_id", "estado", "fecha"):
        op.create_index(f"ix_pedidos_{field}", "pedidos", [field])


def downgrade():
    op.drop_table("pedidos")
    op.drop_table("productos")
    op.drop_table("platillos")
    op.drop_table("cuentas")
