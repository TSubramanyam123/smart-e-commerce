from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.core.config import settings

from app.routers import (
    auth,
    products,
    cart,
    orders,
    payments,
    notifications
)


app = FastAPI(
    title="Smart E-Commerce API",
    description=(
        "Backend API for Smart "
        "E-Commerce Platform"
    ),
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(
    auth.router
)

app.include_router(
    products.router
)

app.include_router(
    cart.router
)

app.include_router(
    orders.router
)

app.include_router(
    payments.router
)

app.include_router(
    notifications.router
)


@app.get("/health")
def health_check():

    return {
        "status": "UP",
        "service": "Smart E-Commerce API"
    }