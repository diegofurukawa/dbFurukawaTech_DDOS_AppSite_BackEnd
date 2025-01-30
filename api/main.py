"""
Main API Module

Initializes the FastAPI application and includes all route modules.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from .bkp import traffic_routes
from .routes import alert_routes, mitigation_routes, user_routes, customer_routes

app = FastAPI(
    title="DDoS Protection API",
    description="API endpoints for DDoS Protection Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://dfurukawatech.ddns.net:3152",
        "http://179.125.208.33:3152",
        "http://192.168.68.111:3000",
        "http://localhost:3000"
        "http://192.168.68.111:3001",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from different modules
app.include_router(alert_routes.router)
app.include_router(mitigation_routes.router)
app.include_router(user_routes.router)
app.include_router(customer_routes.router)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)