from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import check, upload, jobs, library
import logging

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Fact Guard API",
    description="Local-first fact-checking assistant API",
    version="1.0.0",
    debug=settings.debug
)

# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(check.router, prefix="/api", tags=["fact-check"])
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(jobs.router, prefix="/api", tags=["jobs"])
app.include_router(library.router, prefix="/api", tags=["library"])


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Fact Guard API v1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )