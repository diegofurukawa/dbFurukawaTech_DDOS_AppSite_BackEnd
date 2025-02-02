"""
Routes Package

Exports all route modules for easy importing.
"""

from .alert_routes import router as alert_router
from .mitigation_routes import router as mitigation_router
from .user_routes import router as user_router
from .customer_routes import router as customer_router
from .managed_object_routes import router as managed_object_router
from .customer_mo_routes import router as customer_mo_router

__all__ = [
    'alert_router'
    ,'mitigation_router'
    ,'user_router'
    ,'customer_router'
    ,'managed_object_router'
    ,'customer_mo_router'
]