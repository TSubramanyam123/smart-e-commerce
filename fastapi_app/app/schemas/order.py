from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class OrderResponse(BaseModel):

    id: int

    total: Decimal

    payment_status: str

    order_status: str

    created_at: datetime

    class Config:
        from_attributes = True