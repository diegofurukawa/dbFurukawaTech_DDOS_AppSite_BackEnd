# src/services/api/routes/user_routes.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from data.database import DatabaseConnection
from utils.log import create_logger
from ..models.user_model import UserBase, UserCreate, UserResponse, UserAccessRequest

router = APIRouter(prefix="/api/users", tags=["users"])
logger = create_logger("user_routes")

class UserAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def create_user(self, user: UserCreate) -> UserResponse:
        try:
            query = """
            INSERT INTO users (email, name, password_hash, company, role, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, email, name, company, role, is_active, created_at, last_login
            """
            # Aqui você deve implementar a hash da senha antes de salvar
            hashed_password = self._hash_password(user.password)
            
            values = (
                user.email,
                user.name,
                hashed_password,
                user.company,
                user.role,
                datetime.now()
            )
            
            result = self.db.execute_query(query, values)
            return UserResponse(**dict(zip(
                ['id', 'email', 'name', 'company', 'role', 'is_active', 'created_at', 'last_login'],
                result[0]
            )))
            
        except Exception as e:
            self.logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create user")

    async def request_access(self, request: UserAccessRequest) -> dict:
        try:
            query = """
            INSERT INTO access_requests (email, name, company, reason, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, email, name, company, reason, status, created_at
            """
            
            values = (
                request.email,
                request.name,
                request.company,
                request.reason,
                request.status,
                request.created_at
            )
            
            result = self.db.execute_query(query, values)
            return dict(zip(
                ['id', 'email', 'name', 'company', 'reason', 'status', 'created_at'],
                result[0]
            ))
            
        except Exception as e:
            self.logger.error(f"Error creating access request: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create access request")
        


# Initialize API handler
user_api = UserAPI()


# Route definitions

@router.get("/create", response_model=UserCreate)
async def create_user():
    return await user_api.create_user()

@router.get("/request_access", response_model=List[UserAccessRequest])  # Corrigido aqui
async def request_access():
    return await user_api.request_access()