"""
Health check endpoint.
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/alive", response_model=dict)
async def health_alive():
    """Health check for load balancers."""
    return {"status": "alive"}


@router.get("/ready", response_model=dict)
async def health_ready():
    """Health check for readiness."""
    return {"status": "ready"}
