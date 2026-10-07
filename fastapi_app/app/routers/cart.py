from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.security import (
    get_current_user
)

from app.models.product import Product

from app.models.commerce import CartItem

from app.schemas.cart import (
    CartItemRequest,
    QuantityRequest
)


router = APIRouter(
    prefix="/api/cart",
    tags=["Cart"]
)


@router.get("")
def get_cart(
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    items = db.scalars(
        select(CartItem).where(
            CartItem.user_id ==
            current_user.id
        )
    ).all()

    result = []

    total = 0

    for item in items:

        product = db.get(
            Product,
            item.product_id
        )

        if not product:
            continue

        subtotal = (
            float(product.price)
            * item.quantity
        )

        total += subtotal

        result.append({
            "product_id": product.id,
            "name": product.name,
            "price": float(product.price),
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "items": result,
        "total": total
    }


@router.post("/items")
def add_to_cart(
    data: CartItemRequest,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    product = db.get(
        Product,
        data.product_id
    )

    if not product or not product.is_active:

        raise HTTPException(
            404,
            "Product not found"
        )

    if data.quantity > product.stock:

        raise HTTPException(
            400,
            "Insufficient stock"
        )

    item = db.scalar(
        select(CartItem).where(
            CartItem.user_id ==
            current_user.id,
            CartItem.product_id ==
            data.product_id
        )
    )

    if item:

        new_quantity = (
            item.quantity +
            data.quantity
        )

        if new_quantity > product.stock:

            raise HTTPException(
                400,
                "Insufficient stock"
            )

        item.quantity = new_quantity

    else:

        item = CartItem(
            user_id=current_user.id,
            product_id=data.product_id,
            quantity=data.quantity
        )

        db.add(item)

    db.commit()

    return {
        "message": "Product added to cart"
    }


@router.put(
    "/items/{product_id}"
)
def update_cart(
    product_id: int,
    data: QuantityRequest,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    item = db.scalar(
        select(CartItem).where(
            CartItem.user_id ==
            current_user.id,
            CartItem.product_id ==
            product_id
        )
    )

    product = db.get(
        Product,
        product_id
    )

    if not item or not product:

        raise HTTPException(
            404,
            "Cart item not found"
        )

    if data.quantity > product.stock:

        raise HTTPException(
            400,
            "Insufficient stock"
        )

    item.quantity = data.quantity

    db.commit()

    return {
        "message": "Cart updated"
    }


@router.delete(
    "/items/{product_id}"
)
def remove_item(
    product_id: int,
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    item = db.scalar(
        select(CartItem).where(
            CartItem.user_id ==
            current_user.id,
            CartItem.product_id ==
            product_id
        )
    )

    if not item:

        raise HTTPException(
            404,
            "Cart item not found"
        )

    db.delete(item)

    db.commit()

    return {
        "message": "Product removed"
    }


@router.delete("")
def clear_cart(
    current_user=Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    items = db.scalars(
        select(CartItem).where(
            CartItem.user_id ==
            current_user.id
        )
    ).all()

    for item in items:

        db.delete(item)

    db.commit()

    return {
        "message": "Cart cleared"
    }