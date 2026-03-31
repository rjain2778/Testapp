"""
Marriage Gifts API - FastAPI Application.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.config.api_settings import api_config
from app.api.party import party_router
from app.api.guest import guest_router
from app.api.item import item_router
from app.api.contribution import contribution_router
from app.api.invitation import invitation_router
from app.api.health import router as health_router
from app.api.payment import payment_router

# Create FastAPI app
app = FastAPI(
    title="Marriage Gifts API",
    description="API for managing wedding gift registries with overflow adjustment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=api_config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(party_router)
app.include_router(guest_router)
app.include_router(item_router)
app.include_router(contribution_router)
app.include_router(invitation_router)
app.include_router(health_router)
app.include_router(payment_router)

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Marriage Gifts API",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    # Uvicorn settings
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(api_config.port),
        reload=True,
    )
