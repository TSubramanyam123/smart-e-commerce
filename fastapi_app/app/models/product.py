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


class Category(Base):

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    popularity: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )