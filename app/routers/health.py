from fastapi import APIRouter
from datetime import datetime
import time
from app.models.schemas import HealthCheck
from app.core.config import settings

router = APIRouter()

# Store startup time for uptime calculation
startup_time = time.time()

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint for monitoring and load balancers"""
    
    current_time = time.time()
    uptime = current_time - startup_time
    
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version=settings.VERSION,
        uptime=round(uptime, 2)
    )

@router.get("/ready")
async def readiness_check():
    """Readiness check for Kubernetes deployments"""
    
    # Add any readiness checks here (database connections, etc.)
    # For now, just return ready status
    
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "calculator_service": "available",
            "api_endpoints": "available"
        }
    }

@router.get("/live")
async def liveness_check():
    """Liveness check for Kubernetes deployments"""
    
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }