"""
Routes Package

Exports all route modules for easy importing.
"""

from .alert_routes import router as alert_router
from .mitigation_routes import router as mitigation_router
from .user_routes import router as user_router

__all__ = ['alert_router', 'mitigation_router', 'user_router']