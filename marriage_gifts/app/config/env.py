"""
Environment variables management for the Marriage Gifts application.
"""

import os
from typing import Optional


def get_env(
    name: str,
    default: Optional[str] = None,
    cast: type = str
) -> Optional[str]:
    """Get environment variable with default and type casting."""
    value = os.getenv(name, default)
    if value is None and default is None:
        return None
    try:
        if value is not None:
            return cast(value)
    except (ValueError, TypeError):
        pass
    return default


# Core application settings
APP_ENV = get_env("APP_ENV", "development")
APP_DEBUG = get_env("APP_DEBUG", "True", bool) == "True"
APP_NAME = get_env("APP_NAME", "Marriage Gifts Collaborator")

# Django settings
DJANGO_DEBUG = get_env("DJANGO_DEBUG", "True", bool) == "True"
DJANGO_SECRET_KEY = get_env("DJANGO_SECRET_KEY", "dev-secret-key")
DJANGO_DATABASE_URL = get_env("DJANGO_DATABASE_URL", "sqlite:///db.sqlite3")
DJANGO_ALLOWED_HOSTS = get_env("DJANGO_ALLOWED_HOSTS", "*").split(",")

# FastAPI settings
FASTAPI_HOST = get_env("FASTAPI_HOST", "0.0.0.0")
FASTAPI_PORT = get_env("FASTAPI_PORT", "8000", int)
FASTAPI_DEBUG = get_env("FASTAPI_DEBUG", "True", bool) == "True"

# Application settings
APP_CURRENCY = get_env("APP_CURRENCY", "INR")
APP_TIMEZONE = get_env("APP_TIMEZONE", "Asia/Kolkata")

# Redis settings
REDIS_HOST = get_env("REDIS_HOST", "localhost")
REDIS_PORT = get_env("REDIS_PORT", "6379", int)
REDIS_DB = get_env("REDIS_DB", "0", int)

# Email settings
EMAIL_HOST_USER = get_env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = get_env("EMAIL_PORT", "587", int)
EMAIL_USE_TLS = get_env("EMAIL_USE_TLS", "True", bool) == "True"
DEFAULT_FROM_EMAIL = get_env("DEFAULT_FROM_EMAIL", "noreply@marriagegifts.com")

# Payment gateway settings (future)
RAZORPAY_KEY_ID = get_env("RAZORPAY_KEY_ID")
RAZORPAY_SECRET_KEY = get_env("RAZORPAY_SECRET_KEY")
PAYTM_MERCHANT_ID = get_env("PAYTM_MERCHANT_ID")

# S3 settings
AWS_ACCESS_KEY_ID = get_env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET_NAME = get_env("AWS_S3_BUCKET_NAME")

# Feature flags
ENABLE_EMAIL_NOTIFICATIONS = get_env("ENABLE_EMAIL_NOTIFICATIONS", "True", bool) == "True"
ENABLE_SMS_NOTIFICATIONS = get_env("ENABLE_SMS_NOTIFICATIONS", "False", bool) == "False"
ENABLE_PDF_RECEIPTS = get_env("ENABLE_PDF_RECEIPTS", "True", bool) == "True"
