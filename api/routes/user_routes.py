from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import List, Optional
from data.database import DatabaseConnection
from utils.log import create_logger
from utils.auth import (
    get_password_hash, verify_password, create_access_token,
    create_refresh_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from ..models.user_model import (
    UserBase, UserCreate, UserResponse, UserLogin, Token, UserUpdate
)
from ..models.alert_model import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/api/users", tags=["users"])
logger = create_logger("user_routes")

class UserAPI:
    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)
        self.db = DatabaseConnection()
        self.db.connect()

    async def get_user_by_id(self, idUser: int, current_user: dict) -> UserResponse:
        """
        Obtém um usuário específico por ID.
        Apenas administradores podem ver outros usuários.
        Usuários normais só podem ver seus próprios dados.
        """
        try:
            # Verifica permissões
            if current_user['role'] != 'admin' and current_user['idUser'] != idUser:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to view this user"
                )

            query = """
                SELECT idUser, email, nameUser, company, role, active, 
                       createdAt, updatedAt, lastLogin
                FROM users
                WHERE idUser = %s
            """
            
            result = self.db.execute_query(query, (idUser,))
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
                
            return UserResponse(**dict(zip(
                ['idUser', 'email', 'nameUser', 'company', 'role', 'active', 
                 'createdAt', 'updatedAt', 'lastLogin'],
                result[0]
            )))

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error fetching user: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch user")

    async def create_user(self, user: UserCreate) -> UserResponse:
        try:
            # Check if user exists
            result = self.db.execute_query(
                "SELECT idUser FROM users WHERE email = %s",
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
                INSERT INTO users (email, nameUser, password_hash, company, role, createdAt)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING idUser, email, nameUser, company, role, active, createdAt
            """
            result = self.db.execute_query(
                query,
                (user.email, user.nameUser, hashed_password, user.company, user.role, datetime.now())
            )
            
            return UserResponse(**dict(zip(
                ['idUser', 'email', 'nameUser', 'company', 'role', 'active', 'createdAt'],
                result[0]
            )))
            
        except Exception as e:
            self.logger.error(f"Error creating user: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to create user")

    async def update_user(self, idUser: int, user_data: UserUpdate, current_user: dict) -> UserResponse:
        try:
            # Verifica permissões
            if current_user['role'] != 'admin' and current_user['idUser'] != idUser:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to update this user"
                )

            update_fields = []
            values = []
            
            if user_data.nameUser is not None:
                update_fields.append("nameUser = %s")
                values.append(user_data.nameUser)
                
            if user_data.company is not None:
                update_fields.append("company = %s")
                values.append(user_data.company)
                
            if user_data.role is not None:
                if current_user['role'] != 'admin':
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Only administrators can change roles"
                    )
                update_fields.append("role = %s")
                values.append(user_data.role)
                
            if user_data.password is not None:
                update_fields.append("password_hash = %s")
                values.append(get_password_hash(user_data.password))
                
            if user_data.active is not None:
                if current_user['role'] != 'admin':
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Only administrators can change user status"
                    )
                update_fields.append("active = %s")
                values.append(user_data.active)

            if not update_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No fields to update"
                )

            # Adiciona campos de atualização
            update_fields.append("updatedAt = %s")
            values.append(datetime.now())
            values.append(idUser)  # for WHERE clause

            query = f"""
                UPDATE users 
                SET {', '.join(update_fields)}
                WHERE idUser = %s
                RETURNING idUser, email, nameUser, company, role, active, createdAt, updatedAt, lastLogin
            """
            
            result = self.db.execute_query(query, tuple(values))
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
                
            return UserResponse(**dict(zip(
                ['idUser', 'email', 'nameUser', 'company', 'role', 'active', 
                 'createdAt', 'updatedAt', 'lastLogin'],
                result[0]
            )))
            
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Error updating user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user"
            )

    async def login(self, form_data: OAuth2PasswordRequestForm) -> Token:
        try:
            # Find user
            self.logger.info(f"Attempting to find user with email: {form_data.username}")
            query = """
                SELECT idUser, email, nameUser, password_hash, company, role,
                       active, createdAt, lastLogin, refresh_token
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
            columns = ['idUser', 'email', 'nameUser', 'password_hash', 'company', 'role',
                      'active', 'createdAt', 'lastLogin', 'refresh_token']
            
            # Create user dictionary making sure we have all required fields
            user = {}
            for i, column in enumerate(columns):
                try:
                    user[column] = result[0][i] if i < len(result[0]) else None
                except IndexError:
                    user[column] = None
                    
            self.logger.info(f"User data mapped: {user}")

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
                # Update last login usando execute_query para o UPDATE
                update_query = """
                    UPDATE users 
                    SET lastLogin = %s, refresh_token = %s 
                    WHERE idUser = %s
                    RETURNING idUser
                """
                self.db.execute_query(
                    update_query,
                    (datetime.now(), refresh_token, user['idUser'])
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

    async def list_users(self, page: int, page_size: int, current_user: dict) -> PaginatedResponse[UserResponse]:
        """
        Lista usuários com paginação.
        Apenas administradores podem ver todos os usuários.
        Usuários normais só podem ver seus próprios dados.
        """
        try:
            params = PaginationParams(page=page, page_size=page_size)
            
            # Define a base da query dependendo do role do usuário
            if current_user['role'] == 'admin':
                where_clause = ""
                query_params = ()
            else:
                where_clause = "WHERE idUser = %s"
                query_params = (current_user['idUser'],)
            
            # Query para contar o total de registros
            count_query = f"SELECT COUNT(*) FROM users {where_clause}"
            count_result = self.db.execute_query(count_query, query_params)
            total_records = count_result[0][0] if count_result else 0
            
            # Query principal com paginação
            query = f"""
                SELECT idUser, email, nameUser, company, role, active, createdAt, lastLogin
                FROM users
                {where_clause}
                ORDER BY nameUser
                LIMIT %s OFFSET %s
            """
            
            # Adiciona os parâmetros de paginação
            all_params = query_params + (params.page_size, params.offset)
            result = self.db.execute_query(query, all_params)
            
            # Processa os resultados
            users = []
            columns = ['idUser', 'email', 'nameUser', 'company', 'role', 'active', 
                      'createdAt', 'lastLogin']
            
            for row in result:
                user_dict = dict(zip(columns, row))
                users.append(UserResponse(**user_dict))
            
            return PaginatedResponse.create(
                items=users,
                total=total_records,
                params=params
            )
            
        except Exception as e:
            self.logger.error(f"Error listing users: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to list users"
            )

# Initialize API handler
user_api = UserAPI()

# Route definitions
@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get info about the currently logged in user"""
    try:
        user = await user_api.get_user_by_id(current_user['idUser'], current_user)
        return user
    except HTTPException:
        return UserResponse(**current_user)

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

@router.post("/refresh")
async def refresh_token(current_user: dict = Depends(get_current_user)):
    new_access_token = create_access_token(
        data={"sub": current_user['email']},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.get("/{idUser}", response_model=UserResponse)
async def get_user(
    idUser: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific user by ID.
    Only administrators can view other users.
    Regular users can only view their own data.
    """
    return await user_api.get_user_by_id(idUser, current_user)

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    return await user_api.create_user(user)

@router.patch("/{idUser}", response_model=UserResponse)
async def update_user(
    idUser: int,
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update user data.
    Regular users can only update their own data.
    Only administrators can:
    - Update other users' data
    - Change user roles
    - Activate/deactivate users
    """
    return await user_api.update_user(idUser, user_data, current_user)

@router.get("", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista usuários com paginação.
    Apenas administradores podem ver todos os usuários.
    Usuários normais só podem ver seus próprios dados.
    """
    return await user_api.list_users(page, page_size, current_user)