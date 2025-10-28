from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field, SecretStr, Field


class PostgresSettings(BaseSettings):
    USER: str
    PASSWORD: SecretStr
    DB: str
    HOST: str
    PORT: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix = "POSTGRES_",
        extra="ignore"
    )

    @computed_field
    @property
    def ENGINE_URL(self) -> SecretStr:
        return SecretStr(f"postgresql+asyncpg://{self.USER}:{self.PASSWORD.get_secret_value()}@{self.HOST}:{self.PORT}/{self.DB}")

class RedisSettings(BaseSettings):
    # USER: str
    PASSWORD: SecretStr
    DB: str
    HOST: str
    PORT: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix = "REDIS_",
        extra="ignore"
    )

    @computed_field
    @property
    def ENGINE_URL(self) -> SecretStr:
        return SecretStr(f"postgresql+asyncpg://{self.USER}:{self.PASSWORD.get_secret_value()}@{self.HOST}:{self.PORT}/{self.DB}")


# class LogSettings(BaseSettings):
#     ECHO: bool = Field(default=False)
#     LEVEL_API: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(default="WARNING")
#     PATH_API: str = Field(default="./logs")
    
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_prefix = "LOG_",
#         extra="ignore"
#     )

class Settings(BaseSettings):
    POSTGRES: PostgresSettings = Field(default_factory=PostgresSettings)
    REDIS: RedisSettings = Field(default_factory=RedisSettings)
    # LOG: LogSettings = Field(default_factory=LogSettings)
    DEV: bool = Field(default=False)

    APP_HOST: str = "127.0.0.1"
    WORKER_SERVICE_PORT: int = 8000
    ORDER_SERVICE_PORT: int = 8000

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env"
    )



SETTINGS = Settings()
