"""
Atualizar para incluir os novos módulos
"""
from .models.user_model import UserBase, UserCreate, UserResponse, UserAccessRequest
from .routes.user_routes import router as user_router

__all__ = [
    'UserBase',
    'UserCreate',
    'UserResponse',
    'UserAccessRequest',
    'user_router'
]