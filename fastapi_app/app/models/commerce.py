from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Text,
    Numeric,
    Integer,
    ForeignKey,
    Boolean,
    DateTime
)

from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CartItem(Base):

    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1
    )


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    total: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    payment_status: Mapped[str] = mapped_column(
        String(30),
        default="pending"
    )

    order_status: Mapped[str] = mapped_column(
        String(30),
        default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


class OrderItem(Base):

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )


class Payment(Base):

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False
    )

    amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    payment_method: Mapped[str] = mapped_column(
        String(50),
        default="stripe"
    )

    transaction_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


class Notification(Base):

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )