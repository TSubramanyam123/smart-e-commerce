from decimal import Decimal

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy import select, desc

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.security import (
    get_current_user,
    require_roles
)

from app.models.product import Product

from app.models.commerce import (
    CartItem,
    Order,
    OrderItem
)

from app.models.user import User

from app.schemas.order import (
    OrderResponse
)

from app.services.notification import (
    create_notification
)


router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"]
)


@router.post(
    "/checkout",
    response_model=OrderResponse
)
async def checkout(
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    cart_items = db.scalars(
        select(CartItem).where(
            CartItem.user_id ==
            current_user.id
        )
    ).all()

    if not cart_items:

        raise HTTPException(
            400,
            "Cart is empty"
        )

    total = Decimal("0.00")

    validated_items = []

    for cart_item in cart_items:

        product = db.get(
            Product,
            cart_item.product_id
        )

        if (
            not product
            or not product.is_active
        ):

            raise HTTPException(
                400,
                "Product is unavailable"
            )

        if cart_item.quantity > product.stock:

            raise HTTPException(
                400,
                f"Insufficient stock for {product.name}"
            )

        total += (
            Decimal(str(product.price))
            * cart_item.quantity
        )

        validated_items.append(
            (
                cart_item,
                product
            )
        )

    order = Order(
        user_id=current_user.id,
        total=total,
        payment_status="pending",
        order_status="pending"
    )

    db.add(order)

    db.flush()

    for cart_item, product in validated_items:

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=cart_item.quantity,
            unit_price=product.price
        )

        db.add(order_item)

    db.commit()

    db.refresh(order)

    await create_notification(
        db=db,
        user_id=current_user.id,
        notification_type="ORDER_CREATED",
        message=(
            f"Order #{order.id} "
            "has been created."
        ),
        email=current_user.email
    )

    return order


@router.get(
    "",
    response_model=list[OrderResponse]
)
def get_my_orders(
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    return db.scalars(
        select(Order)
        .where(
            Order.user_id ==
            current_user.id
        )
        .order_by(
            desc(Order.created_at)
        )
    ).all()


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    order = db.get(
        Order,
        order_id
    )

    if (
        not order
        or order.user_id != current_user.id
    ):

        raise HTTPException(
            404,
            "Order not found"
        )

    return order


@router.put(
    "/{order_id}/status"
)
async def update_order_status(
    order_id: int,
    status: str,
    current_user=Depends(
        require_roles(
            "admin",
            "staff"
        )
    ),
    db: Session = Depends(get_db)
):

    allowed_statuses = {
        "pending",
        "confirmed",
        "processing",
        "shipped",
        "out_for_delivery",
        "delivered",
        "cancelled"
    }

    if status not in allowed_statuses:

        raise HTTPException(
            400,
            "Invalid order status"
        )

    order = db.get(
        Order,
        order_id
    )

    if not order:

        raise HTTPException(
            404,
            "Order not found"
        )

    order.order_status = status

    db.commit()

    customer = db.get(
        User,
        order.user_id
    )

    await create_notification(
        db,
        order.user_id,
        "ORDER_STATUS",
        (
            f"Order #{order.id} "
            f"status changed to {status}."
        ),
        customer.email if customer else None
    )

    return {
        "message": "Order status updated",
        "order_id": order.id,
        "status": order.order_status
    }