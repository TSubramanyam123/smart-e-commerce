from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):

    name: str

    description: str | None = None

    price: Decimal = Field(
        gt=0
    )

    stock: int = Field(
        ge=0
    )

    category_id: int | None = None

    image_url: str | None = None


class ProductResponse(ProductCreate):

    id: int

    popularity: int

    is_active: bool

    class Config:
        from_attributes = True