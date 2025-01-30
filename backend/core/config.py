from pathlib import Path

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    # Application settings
    app_env: str = "development"

    # Auth
    secret_key: str = "SECRET_KEY"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 1000
    algorithm: str = "HS256"

    # Email settings
    # email_signup_confirmation_token_expire_hours: int = 1
    # mail_from: str
    # mail_password: str
    # mail_port: int
    # mail_server: str
    # hostname: str = "localhost"

    # Database settings
    db_driver: str = "postgresql+asyncpg"
    db_name: str = Field(default="db_name", alias="POSTGRES_DB")
    db_user: str = Field(default="user", alias="POSTGRES_USER")
    db_password: str = Field(default="password", alias="POSTGRES_PASSWORD")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = 5432

    # Google authentication settings
    # google_client_id: str
    # google_client_secret: str
    # google_redirect_url: str

    # GitHub authentication settings
    # github_client_id: str
    # github_client_secret: str
    # github_redirect_url: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent.joinpath(".env"),
        env_file_encoding="utf-8",
    )

    @computed_field
    @property
    def db_url(self) -> URL:
        """
        Computed property to get SQLAlchemy URL, using env settings
        """
        return URL.create(
            drivername=self.db_driver,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            database=self.db_name,
            port=self.db_port,
        )


# Create a singleton instance of the settings
settings = Settings()
