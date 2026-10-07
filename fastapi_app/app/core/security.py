from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from passlib.context import CryptContext

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db

from app.models.user import User


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Swagger will now show:
# Value: Bearer <your-token>
security = HTTPBearer()


def hash_password(password: str):

    return password_context.hash(password)


def verify_password(
    password: str,
    password_hash: str
):

    return password_context.verify(
        password,
        password_hash
    )


def create_access_token(
    user_id: int,
    role: str
):

    expiration = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expiration
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[
                settings.jwt_algorithm
            ]
        )

        user_id = int(
            payload.get("sub")
        )

    except (
        JWTError,
        TypeError,
        ValueError
    ):

        raise credentials_exception

    user = db.get(
        User,
        user_id
    )

    if not user or not user.is_active:

        raise credentials_exception

    return user


def require_roles(*roles):

    def role_checker(
        current_user=Depends(
            get_current_user
        )
    ):

        if current_user.role not in roles:

            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )

        return current_user

    return role_checker