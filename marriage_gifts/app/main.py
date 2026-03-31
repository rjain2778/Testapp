"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, get_db
from app.config.api_settings import api_config

# Create FastAPI app
app = FastAPI(
    title=api_config.title,
    description=api_config.description,
    version=api_config.version,
    debug=api_config.debug,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=api_config.allow_origins,
    allow_credentials=api_config.allow_credentials,
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()
    print(f"Marriage Gifts API started on {api_config.host}:{api_config.port}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Marriage Gifts API",
        "version": api_config.version,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include routers
from app.routers import party, guest, item, contribution
from app.routers import invitation

app.include_router(party.router, prefix="/api/parties", tags=["Parties"])
app.include_router(guest.router, prefix="/api/guests", tags=["Guests"])
app.include_router(item.router, prefix="/api/items", tags=["Items"])
app.include_router(contribution.router, prefix="/api/contributions", tags=["Contributions"])
app.include_router(invitation.router, prefix="/api/invitations", tags=["Invitations"])
