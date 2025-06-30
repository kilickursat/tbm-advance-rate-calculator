from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.routers import calculator, health
from app.core.config import settings
from app.core.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting TBM Advance Rate Calculator API")
    yield
    # Shutdown
    logger.info("Shutting down TBM Advance Rate Calculator API")

app = FastAPI(
    title="TBM Advance Rate Calculator",
    description="Production-ready API for calculating tunnel boring machine advance rates based on geological and operational parameters",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(calculator.router, prefix="/api/v1", tags=["calculator"])

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main application page"""
    with open("app/static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
