"""Initial schema: all Vantier tables and enums.

Revision ID: 20260409_001
Revises: (none — baseline)
Create Date: 2026-04-09
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260409_001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------------------------------------------------------------ Enums
    op.execute("CREATE TYPE admin_role AS ENUM ('owner', 'operative')")
    op.execute("CREATE TYPE product_line AS ENUM ('polo_atelier', 'signature', 'essential')")
    op.execute("CREATE TYPE product_style AS ENUM ('classic', 'design')")
    op.execute("CREATE TYPE product_size AS ENUM ('S', 'M', 'L', 'XL', 'XXL', 'XXXL')")
    op.execute("CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled')")
    op.execute("CREATE TYPE payment_status AS ENUM ('pending', 'paid', 'failed', 'refunded')")
    op.execute("CREATE TYPE discount_type AS ENUM ('percent', 'fixed')")
    op.execute("CREATE TYPE exchange_status AS ENUM ('requested', 'approved', 'shipped', 'completed', 'rejected')")
    op.execute("CREATE TYPE po_status AS ENUM ('ordered', 'in_transit', 'received')")

    # ------------------------------------------------------------ admin_users
    op.create_table(
        "admin_users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("neon_auth_user_id", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("role", postgresql.ENUM("owner", "operative", name="admin_role", create_type=False), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("neon_auth_user_id"),
        sa.UniqueConstraint("email"),
    )

    # --------------------------------------------------------------- products
    op.create_table(
        "products",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("line", postgresql.ENUM("polo_atelier", "signature", "essential", name="product_line", create_type=False), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )

    # -------------------------------------------------------- product_variants
    op.create_table(
        "product_variants",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("style", postgresql.ENUM("classic", "design", name="product_style", create_type=False), nullable=False),
        sa.Column("size", postgresql.ENUM("S", "M", "L", "XL", "XXL", "XXXL", name="product_size", create_type=False), nullable=False),
        sa.Column("color", sa.String(100), nullable=False),
        sa.Column("sku", sa.String(100), nullable=False),
        sa.Column("barcode", sa.String(100), nullable=False),
        sa.Column("stock_qty", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("cost_acquisition_usd", sa.Numeric(10, 2), nullable=False),
        sa.Column("price_usd", sa.Numeric(10, 2), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sku"),
        sa.UniqueConstraint("barcode"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.CheckConstraint("stock_qty >= 0", name="ck_variant_stock_non_negative"),
        sa.CheckConstraint("cost_acquisition_usd >= 0", name="ck_variant_cost_non_negative"),
        sa.CheckConstraint("price_usd > 0", name="ck_variant_price_positive"),
    )
    op.create_index("ix_product_variants_product_id", "product_variants", ["product_id"])
    op.create_index("ix_product_variants_sku", "product_variants", ["sku"])
    op.create_index("ix_product_variants_barcode", "product_variants", ["barcode"])

    # --------------------------------------------------------- product_images
    op.create_table(
        "product_images",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("variant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("position", sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("alt_text", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["variant_id"], ["product_variants.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_product_images_variant_position", "product_images", ["variant_id", "position"])

    # -------------------------------------------------------- saved_addresses
    op.create_table(
        "saved_addresses",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("neon_auth_user_id", sa.String(), nullable=False),
        sa.Column("label", sa.String(100), nullable=True),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("line1", sa.String(255), nullable=False),
        sa.Column("line2", sa.String(255), nullable=True),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("state", sa.String(100), nullable=True),
        sa.Column("zip", sa.String(20), nullable=False),
        sa.Column("country", sa.String(2), nullable=False),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_saved_addresses_user", "saved_addresses", ["neon_auth_user_id"])

    # -------------------------------------------------------- discount_codes
    op.create_table(
        "discount_codes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("code", sa.String(100), nullable=False),
        sa.Column("type", postgresql.ENUM("percent", "fixed", name="discount_type", create_type=False), nullable=False),
        sa.Column("value", sa.Numeric(10, 2), nullable=False),
        sa.Column("usage_limit", sa.Integer(), nullable=True),
        sa.Column("usage_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.CheckConstraint("value > 0", name="ck_discount_value_positive"),
        sa.CheckConstraint("usage_count >= 0", name="ck_discount_usage_count_non_negative"),
    )

    # ----------------------------------------------------------------- orders
    op.create_table(
        "orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("neon_auth_user_id", sa.String(), nullable=True),
        sa.Column("customer_email", sa.String(), nullable=False),
        sa.Column("customer_name", sa.String(255), nullable=True),
        sa.Column("status", postgresql.ENUM("pending", "processing", "shipped", "delivered", "cancelled", name="order_status", create_type=False), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("payment_status", postgresql.ENUM("pending", "paid", "failed", "refunded", name="payment_status", create_type=False), nullable=False, server_default=sa.text("'pending'")),
        sa.Column("subtotal_usd", sa.Numeric(10, 2), nullable=False),
        sa.Column("shipping_usd", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("discount_usd", sa.Numeric(10, 2), nullable=False, server_default=sa.text("0")),
        sa.Column("total_usd", sa.Numeric(10, 2), nullable=False),
        sa.Column("shipping_address", postgresql.JSONB(), nullable=False),
        sa.Column("is_free_shipping", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("stripe_payment_intent_id", sa.String(), nullable=True),
        sa.Column("stripe_checkout_session_id", sa.String(), nullable=True),
        sa.Column("carrier_tracking_number", sa.String(), nullable=True),
        sa.Column("envia_shipment_id", sa.String(), nullable=True),
        sa.Column("envia_label_url", sa.Text(), nullable=True),
        sa.Column("discount_code_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["discount_code_id"], ["discount_codes.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_orders_neon_auth_user_id", "orders", ["neon_auth_user_id"])
    op.create_index("ix_orders_status", "orders", ["status"])
    op.create_index("ix_orders_payment_status", "orders", ["payment_status"])
    op.create_index("ix_orders_stripe_payment_intent_id", "orders", ["stripe_payment_intent_id"])
    op.create_index("ix_orders_created_at", "orders", ["created_at"])

    # -------------------------------------------------------------- order_items
    op.create_table(
        "order_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("variant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.Column("unit_price_usd", sa.Numeric(10, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["variant_id"], ["product_variants.id"], ondelete="RESTRICT"),
        sa.CheckConstraint("qty > 0", name="ck_order_item_qty_positive"),
    )
    op.create_index("ix_order_items_order_id", "order_items", ["order_id"])
    op.create_index("ix_order_items_variant_id", "order_items", ["variant_id"])

    # --------------------------------------------------------------- exchanges
    op.create_table(
        "exchanges",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("original_variant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("replacement_variant_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("status", postgresql.ENUM("requested", "approved", "shipped", "completed", "rejected", name="exchange_status", create_type=False), nullable=False, server_default=sa.text("'requested'")),
        sa.Column("customer_notes", sa.Text(), nullable=True),
        sa.Column("admin_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["original_variant_id"], ["product_variants.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["replacement_variant_id"], ["product_variants.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_exchanges_order_id", "exchanges", ["order_id"])
    op.create_index("ix_exchanges_status", "exchanges", ["status"])

    # --------------------------------------------------------- purchase_orders
    op.create_table(
        "purchase_orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("reference_number", sa.String(50), nullable=False),
        sa.Column("supplier_name", sa.String(200), nullable=False),
        sa.Column("expected_arrival_date", sa.Date(), nullable=True),
        sa.Column("status", postgresql.ENUM("ordered", "in_transit", "received", name="po_status", create_type=False), nullable=False, server_default=sa.text("'ordered'")),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("reference_number"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["admin_users.id"], ondelete="SET NULL"),
    )

    # ----------------------------------------------------- purchase_order_items
    op.create_table(
        "purchase_order_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("po_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("variant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("qty_ordered", sa.Integer(), nullable=False),
        sa.Column("qty_received", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["po_id"], ["purchase_orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["variant_id"], ["product_variants.id"], ondelete="RESTRICT"),
        sa.CheckConstraint("qty_ordered > 0", name="ck_po_item_qty_ordered_positive"),
        sa.CheckConstraint("qty_received >= 0", name="ck_po_item_qty_received_non_negative"),
    )
    op.create_index("ix_po_items_po_id", "purchase_order_items", ["po_id"])
    op.create_index("ix_po_items_variant_id", "purchase_order_items", ["variant_id"])

    # --------------------------------------------------------- operating_costs
    op.create_table(
        "operating_costs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("label", sa.String(200), nullable=False),
        sa.Column("amount_usd", sa.Numeric(10, 2), nullable=False),
        sa.Column("is_recurring", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("amount_usd > 0", name="ck_op_cost_amount_positive"),
    )


def downgrade() -> None:
    op.drop_table("operating_costs")
    op.drop_table("purchase_order_items")
    op.drop_table("purchase_orders")
    op.drop_table("exchanges")
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("discount_codes")
    op.drop_table("saved_addresses")
    op.drop_table("product_images")
    op.drop_table("product_variants")
    op.drop_table("products")
    op.drop_table("admin_users")

    op.execute("DROP TYPE IF EXISTS po_status")
    op.execute("DROP TYPE IF EXISTS exchange_status")
    op.execute("DROP TYPE IF EXISTS discount_type")
    op.execute("DROP TYPE IF EXISTS payment_status")
    op.execute("DROP TYPE IF EXISTS order_status")
    op.execute("DROP TYPE IF EXISTS product_size")
    op.execute("DROP TYPE IF EXISTS product_style")
    op.execute("DROP TYPE IF EXISTS product_line")
    op.execute("DROP TYPE IF EXISTS admin_role")
