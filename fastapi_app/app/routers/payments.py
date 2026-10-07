from decimal import Decimal

import json
import stripe

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user

from app.models.product import Product

from app.models.commerce import (
    Order,
    OrderItem,
    Payment
)

from app.models.user import User

from app.services.notification import (
    create_notification
)


router = APIRouter(
    prefix="/api/payments",
    tags=["Payments"]
)


if settings.stripe_secret_key:

    stripe.api_key = (
        settings.stripe_secret_key
    )


@router.post(
    "/create/{order_id}"
)
def create_payment(
    order_id: int,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    if not settings.stripe_secret_key:

        raise HTTPException(
            503,
            "Stripe is not configured"
        )

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

    if order.payment_status == "paid":

        raise HTTPException(
            400,
            "Order is already paid"
        )

    order_items = db.scalars(
        select(OrderItem).where(
            OrderItem.order_id ==
            order.id
        )
    ).all()

    line_items = []

    for item in order_items:

        product = db.get(
            Product,
            item.product_id
        )

        if not product:

            raise HTTPException(
                400,
                "Product not found"
            )

        line_items.append({
            "price_data": {
                "currency": "inr",
                "product_data": {
                    "name": product.name
                },
                "unit_amount": int(
                    Decimal(
                        str(item.unit_price)
                    ) * 100
                )
            },
            "quantity": item.quantity
        })

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=line_items,
        success_url=(
            settings.stripe_success_url
        ),
        cancel_url=(
            settings.stripe_cancel_url
        ),
        metadata={
            "order_id": str(order.id),
            "user_id": str(current_user.id)
        }
    )

    payment = Payment(
        order_id=order.id,
        amount=order.total,
        payment_method="stripe",
        transaction_id=session.id,
        status="pending"
    )

    db.add(payment)

    db.commit()

    return {
        "checkout_url": session.url,
        "session_id": session.id
    }


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):

    payload = await request.body()

    signature = request.headers.get(
        "stripe-signature"
    )

    try:

        if settings.stripe_webhook_secret:

            event = (
                stripe.Webhook.construct_event(
                    payload,
                    signature,
                    settings.stripe_webhook_secret
                )
            )

        else:

            event = stripe.Event.construct_from(
                json.loads(payload),
                stripe.api_key
            )

    except Exception as exception:

        raise HTTPException(
            400,
            f"Invalid webhook: {exception}"
        )

    if event["type"] == (
        "checkout.session.completed"
    ):

        session = (
            event["data"]["object"]
        )

        metadata = session.get(
            "metadata",
            {}
        )

        order_id = int(
            metadata["order_id"]
        )

        order = db.get(
            Order,
            order_id
        )

        if (
            order
            and order.payment_status != "paid"
        ):

            order.payment_status = "paid"

            order.order_status = "confirmed"

            payment = db.scalar(
                select(Payment).where(
                    Payment.transaction_id ==
                    session["id"]
                )
            )

            if payment:

                payment.status = "success"

            order_items = db.scalars(
                select(OrderItem).where(
                    OrderItem.order_id ==
                    order.id
                )
            ).all()

            for item in order_items:

                product = db.get(
                    Product,
                    item.product_id
                )

                if product:

                    product.stock -= (
                        item.quantity
                    )

                    product.popularity += (
                        item.quantity
                    )

            db.commit()

            user = db.get(
                User,
                order.user_id
            )

            await create_notification(
                db,
                order.user_id,
                "PAYMENT_SUCCESS",
                (
                    f"Payment successful. "
                    f"Order #{order.id} "
                    "has been confirmed."
                ),
                user.email
                if user else None
            )

    return {
        "received": True
    }