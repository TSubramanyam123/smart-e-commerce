from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

from app.models.user import User

from app.schemas.auth import (
    RegisterRequest,
    LoginResponse
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=LoginResponse
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    email = data.email.lower()

    existing_user = db.scalar(
        select(User).where(
            User.email == email
        )
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    user = User(
        name=data.name,
        email=email,
        password_hash=hash_password(
            data.password
        ),
        role="customer"
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    token = create_access_token(
        user.id,
        user.role
    )

    return LoginResponse(
        access_token=token
    )


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.scalar(
        select(User).where(
            User.email == form.username.lower()
        )
    )

    if (
        not user
        or not user.password_hash
        or not verify_password(
            form.password,
            user.password_hash
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        user.id,
        user.role
    )

    return LoginResponse(
        access_token=token
    )


@router.get("/me")
def get_me(
    current_user: User = Depends(
        get_current_user
    )
):

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }