from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy import (
    select,
    asc,
    desc
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.security import (
    require_roles
)

from app.models.product import Product

from app.schemas.product import (
    ProductCreate,
    ProductResponse
)


router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)


@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_products(
    category_id: int | None = None,
    min_price: float | None = Query(
        default=None,
        ge=0
    ),
    max_price: float | None = Query(
        default=None,
        ge=0
    ),
    sort: str = "popularity",
    db: Session = Depends(get_db)
):

    query = select(Product).where(
        Product.is_active.is_(True)
    )

    if category_id:

        query = query.where(
            Product.category_id == category_id
        )

    if min_price is not None:

        query = query.where(
            Product.price >= min_price
        )

    if max_price is not None:

        query = query.where(
            Product.price <= max_price
        )

    if sort == "price_asc":

        query = query.order_by(
            asc(Product.price)
        )

    elif sort == "price_desc":

        query = query.order_by(
            desc(Product.price)
        )

    else:

        query = query.order_by(
            desc(Product.popularity)
        )

    return db.scalars(query).all()


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.get(
        Product,
        product_id
    )

    if not product or not product.is_active:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.post(
    "",
    response_model=ProductResponse
)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "admin",
            "staff"
        )
    )
):

    product = Product(
        **data.model_dump()
    )

    db.add(product)

    db.commit()

    db.refresh(product)

    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            "admin",
            "staff"
        )
    )
):

    product = db.get(
        Product,
        product_id
    )

    if not product:

        raise HTTPException(
            404,
            "Product not found"
        )

    for key, value in data.model_dump().items():

        setattr(
            product,
            key,
            value
        )

    db.commit()

    db.refresh(product)

    return product


@router.delete(
    "/{product_id}"
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("admin")
    )
):

    product = db.get(
        Product,
        product_id
    )

    if not product:

        raise HTTPException(
            404,
            "Product not found"
        )

    product.is_active = False

    db.commit()

    return {
        "message": "Product deleted"
    }