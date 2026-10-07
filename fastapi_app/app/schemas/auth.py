from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):

    name: str

    email: EmailStr

    password: str = Field(
        min_length=8
    )


class LoginResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"