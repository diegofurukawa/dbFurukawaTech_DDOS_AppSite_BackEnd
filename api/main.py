"""
Main API Module

Initializes the FastAPI application and includes all route modules.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from data.database import DatabaseConnection
from utils.log import create_logger

# from .bkp import traffic_routes
from .routes import (
    alert_routes
    ,company_routes
    ,customer_routes
    ,customer_mo_routes
    ,customer_dashboard_routes
    ,managed_object_routes
    ,mitigation_routes
    ,user_routes
)

# Configure logger
logger = create_logger("main")

app = FastAPI(
    title="DDoS Protection API",
    description="API endpoints for DDoS Protection Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        #Producao
        "http://dfurukawatech.ddns.net:3152",
        "http://179.125.208.33:3152",

        #Desenvolvimento
        "http://192.168.68.111:3000",
        "http://localhost:3000"
        # "http://192.168.68.111:3001",
        # "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from different modules
app.include_router(alert_routes.router)
app.include_router(company_routes.router)
app.include_router(customer_routes.router)
app.include_router(customer_mo_routes.router)
app.include_router(customer_dashboard_routes.router)
app.include_router(managed_object_routes.router)
app.include_router(mitigation_routes.router)
app.include_router(user_routes.router)

@app.on_event("startup")
async def startup_event():
    """Initialize connection pool and other startup tasks"""
    try:
        logger.info("Initializing database connection pool...")
        DatabaseConnection.init_pool()
        logger.info("Database connection pool initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database connection pool: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup tasks before shutdown"""
    try:
        logger.info("Closing database connection pool...")
        DatabaseConnection.dispose_pool()
        logger.info("Database connection pool closed successfully")
    except Exception as e:
        logger.error(f"Error closing database connection pool: {e}")

# Root redirect to docs
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint that also verifies database connectivity"""
    try:
        with DatabaseConnection() as db:
            db.execute_query("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting DDoS Protection API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)