from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    commerce_store_id = Column(Integer, nullable=True)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False, index=True)
    customer_phone = Column(String(50), nullable=True)
    shipping_address = Column(String(500), nullable=True)
    shipping_address2 = Column(String(500), nullable=True)
    shipping_city = Column(String(255), nullable=True)
    shipping_postcode = Column(String(50), nullable=True)
    shipping_country = Column(String(100), nullable=True)
    subtotal = Column(Numeric(12, 2), nullable=False, default=0)
    total = Column(Numeric(12, 2), nullable=False, default=0)
    currency = Column(String(10), nullable=False, default="nzd")
    status = Column(String(50), nullable=False, default="pending", index=True)
    stripe_session_id = Column(String(500), unique=True, nullable=True, index=True)
    stripe_payment_intent_id = Column(String(500), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id = Column(String(100), nullable=True)
    sku = Column(String(255), nullable=True)
    product_name = Column(String(500), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(12, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
