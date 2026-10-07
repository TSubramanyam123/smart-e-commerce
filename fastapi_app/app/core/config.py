from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""

    stripe_success_url: str = "http://localhost:3000/payment/success"
    stripe_cancel_url: str = "http://localhost:3000/payment/cancel"

    auth0_domain: str = ""
    auth0_audience: str = ""

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "no-reply@example.com"
    smtp_use_tls: bool = True

    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def cors_origin_list(self):
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()