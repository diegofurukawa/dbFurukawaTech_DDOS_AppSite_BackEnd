"""
Routes Package

Exports all route modules for easy importing.
"""

from .alert_model import Alert, AlertStats, AlertTop, AlertTrafficData, PaginatedResponse, PaginationParams
from .mitigation_model import MitigationBase, MitigationTrafficPoint, MitigationStats
from .user_model import UserBase, UserCreate, UserLogin, Token, TokenData, UserResponse

__all__ = [
    # Alerts
    'UserBase'
    ,'UserCreate'
    ,'UserResponse' 
    ,'UserLogin'
    ,'Token'
    ,'TokenData'

    # Alerts
    'Alert'
    ,'AlertStats'
    ,'AlertTop' 
    ,'AlertTrafficData'
    ,'PaginatedResponse'
    ,'PaginationParams'

    # Mitigation
    ,'MitigationBase'
    ,'MitigationStats'
    ,'MitigationTrafficPoint'
]