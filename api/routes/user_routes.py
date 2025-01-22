from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import List
from data.database import DatabaseConnection
from utils.log import create_logger
from utils.auth import (
    get_password_hash, verify_password, create_access_token,
    create_refresh_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from ..models.user_model import (
    UserBase, UserCreate, UserResponse, UserLogin, Token
)

router = APIRouter(prefix="/api/users", tags=["users"])
logger = create_logger("user_routes")

class UserAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def create_user(self, user: UserCreate) -> UserResponse:
        try:
            # Check if user exists
            result = self.db.execute_query(
                "SELECT id FROM users WHERE email = %s",
                (user.email,)
            )
            if result:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )

            # Create new user
            hashed_password = get_password_hash(user.password)
            query = """
                INSERT INTO users (email, name, password_hash, company, role)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, email, name, company, role, is_active, created_at
            """
            result = self.db.execute_query(
                query,
                (user.email, user.name, hashed_password, user.company, user.role)
            )
            
            return UserResponse(**dict(zip(
                ['id', 'email', 'name', 'company', 'role', 'is_active', 'created_at'],
                result[0]
            )))
            
        except Exception as e:
            self.logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create user")

    async def login(self, form_data: OAuth2PasswordRequestForm) -> Token:
        try:
            # Find user
            self.logger.info(f"Attempting to find user with email: {form_data.username}")
            query = """
                SELECT id, email, name, password_hash, company, role,
                       is_active, created_at, last_login, refresh_token
                FROM users 
                WHERE email = %s
            """
            self.logger.info(f"Executing query: {query} with params: {form_data.username}")
            result = self.db.execute_query(query, (form_data.username,))
            self.logger.info(f"Query result: {result}")
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                )

            # Get column names from the query result
            columns = ['id', 'email', 'name', 'password_hash', 'company', 'role',
                      'is_active', 'created_at', 'last_login', 'refresh_token']
            
            # Create user dictionary making sure we have all required fields
            user = {}
            for i, column in enumerate(columns):
                try:
                    user[column] = result[0][i] if i < len(result[0]) else None
                except IndexError:
                    user[column] = None
                    
            self.logger.info(f"User data mapped: {user}")  # Log para debug

            self.logger.info(f"Verifying password for user: {user['email']}")
            if not user.get('password_hash'):
                self.logger.error("No password hash found for user")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User authentication error",
                )

            self.logger.info(f"Password hash from DB: {user['password_hash']}")
            self.logger.info(f"Attempting to verify password")
            
            try:
                is_valid = verify_password(form_data.password, user['password_hash'])
                self.logger.info(f"Password verification result: {is_valid}")
                
                if not is_valid:
                    self.logger.error("Password verification failed")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect email or password",
                    )
            except Exception as e:
                self.logger.error(f"Error during password verification: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error verifying password",
                )

            # Create tokens
            access_token = create_access_token(
                data={"sub": user['email']},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            refresh_token = create_refresh_token(data={"sub": user['email']})

            try:
                # Update last login
                update_query = """
                    UPDATE users 
                    SET last_login = %s, refresh_token = %s 
                    WHERE id = %s
                """
                self.db.execute_update(
                    update_query,
                    (datetime.now(), refresh_token, user['id'])
                )
                
                return Token(
                    access_token=access_token,
                    token_type="bearer",
                    refresh_token=refresh_token
                )
            
            except Exception as e:
                self.logger.error(f"Error updating user login info: {str(e)}")
                # Mesmo se falhar a atualização, ainda retornamos o token
                return Token(
                    access_token=access_token,
                    token_type="bearer",
                    refresh_token=refresh_token
                )

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error during login: {str(e)}")
            raise HTTPException(status_code=500, detail="Login failed")

# Initialize API handler
user_api = UserAPI()

# Route definitions
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    return await user_api.create_user(user)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        return await user_api.login(form_data)
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return UserResponse(**current_user)

@router.post("/refresh")
async def refresh_token(current_user: dict = Depends(get_current_user)):
    new_access_token = create_access_token(
        data={"sub": current_user['email']},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": new_access_token, "token_type": "bearer"}