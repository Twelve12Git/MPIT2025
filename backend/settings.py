from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "OrderService"
    debug: bool = False
    order_service_host: str = "0.0.0.0"
    order_service_port: int = 8000

    worker_service_host: str = "0.0.0.0"
    worker_service_port: int = 8001
    
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    @property
    def redis_url(self) -> str:
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()