"""
FastAPI settings for the Marriage Gifts application.
"""

from pydantic import BaseModel, Field
from typing import List


class APIConfig(BaseModel):
    """FastAPI application configuration."""

    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    title: str = "Marriage Gifts API"
    description: str = "API for managing marriage gift contributions"
    version: str = "1.0.0"

    # CORS
    allow_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"]
    )
    allow_credentials: bool = True

    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_minutes: int = 10080

    # Database
    database_url: str = "sqlite:///./database.db"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    # Payment gateways (future)
    razorpay_key_id: str = ""
    razorpay_secret_key: str = ""
    paytm_merchant_id: str = ""

    # S3/Cloud Storage
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_s3_bucket_name: str = ""

    class Config:
        env_file = ".env"


# Create instance
api_config = APIConfig()
