from pydantic import BaseModel, Field


class CartItemRequest(BaseModel):

    product_id: int

    quantity: int = Field(
        gt=0
    )


class QuantityRequest(BaseModel):

    quantity: int = Field(
        gt=0
    )