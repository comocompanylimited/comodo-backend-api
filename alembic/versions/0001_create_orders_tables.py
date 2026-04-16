"""create orders and order_items tables

Revision ID: 0001
Revises:
Create Date: 2026-04-16
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        commerce_store_id INTEGER,
        customer_name VARCHAR(255) NOT NULL,
        customer_email VARCHAR(255) NOT NULL,
        customer_phone VARCHAR(50),
        shipping_address VARCHAR(500),
        shipping_address2 VARCHAR(500),
        shipping_city VARCHAR(255),
        shipping_postcode VARCHAR(50),
        shipping_country VARCHAR(100),
        subtotal NUMERIC(12,2) NOT NULL DEFAULT 0,
        total NUMERIC(12,2) NOT NULL DEFAULT 0,
        currency VARCHAR(10) NOT NULL DEFAULT 'nzd',
        status VARCHAR(50) NOT NULL DEFAULT 'pending',
        stripe_session_id VARCHAR(500) UNIQUE,
        stripe_payment_intent_id VARCHAR(500),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_orders_customer_email ON orders (customer_email)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_orders_status ON orders (status)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_orders_stripe_session_id ON orders (stripe_session_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_orders_stripe_payment_intent_id ON orders (stripe_payment_intent_id)")

    op.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
        product_id VARCHAR(100),
        sku VARCHAR(255),
        product_name VARCHAR(500) NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        unit_price NUMERIC(12,2) NOT NULL,
        total_price NUMERIC(12,2) NOT NULL
    )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_order_items_order_id ON order_items (order_id)")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS order_items CASCADE")
    op.execute("DROP TABLE IF EXISTS orders CASCADE")
