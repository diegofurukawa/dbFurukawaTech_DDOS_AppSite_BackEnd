from fastapi import APIRouter, HTTPException, Depends, status, Query
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
                    SET last_login = %s, refresh_token = %s 
                    WHERE id = %s
                    RETURNING id
                """
                self.db.execute_query(
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

    async def update_user(self, user_id: int, user_data: UserUpdate, current_user: dict) -> UserResponse:
        """
        Atualiza os dados de um usuário.
        Apenas administradores podem atualizar outros usuários.
        Usuários normais só podem atualizar seus próprios dados.
        """
        try:
            # Verifica permissões
            if current_user['role'] != 'admin' and current_user['id'] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to update this user"
                )

            # Prepara os campos para atualização
            update_fields = []
            values = []
            
            if user_data.name is not None:
                update_fields.append("name = %s")
                values.append(user_data.name)
                
            if user_data.company is not None:
                update_fields.append("company = %s")
                values.append(user_data.company)
                
            if user_data.role is not None:
                # Apenas admin pode mudar roles
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
                
            if user_data.is_active is not None:
                # Apenas admin pode ativar/desativar usuários
                if current_user['role'] != 'admin':
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Only administrators can change user status"
                    )
                update_fields.append("is_active = %s")
                values.append(user_data.is_active)

            if not update_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No fields to update"
                )

            # Adiciona o ID do usuário aos valores
            values.append(user_id)

            # Constrói e executa a query
            query = f"""
                UPDATE users 
                SET {', '.join(update_fields)}
                WHERE id = %s
                RETURNING id, email, name, company, role, is_active, created_at, last_login
            """
            
            result = self.db.execute_query(query, tuple(values))
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
                
            return UserResponse(**dict(zip(
                ['id', 'email', 'name', 'company', 'role', 'is_active', 'created_at', 'last_login'],
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
                where_clause = "WHERE id = %s"
                query_params = (current_user['id'],)
            
            # Query para contar o total de registros
            count_query = f"SELECT COUNT(*) FROM users {where_clause}"
            count_result = self.db.execute_query(count_query, query_params)
            total_records = count_result[0][0] if count_result else 0
            
            # Query principal com paginação
            query = f"""
                SELECT id, email, name, company, role, is_active, created_at, last_login
                FROM users
                {where_clause}
                ORDER BY name
                LIMIT %s OFFSET %s
            """
            
            # Adiciona os parâmetros de paginação
            all_params = query_params + (params.page_size, params.offset)
            result = self.db.execute_query(query, all_params)
            
            # Processa os resultados
            users = []
            columns = ['id', 'email', 'name', 'company', 'role', 'is_active', 
                      'created_at', 'last_login']
            
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

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza os dados de um usuário.
    
    - Usuários normais só podem atualizar seus próprios dados
    - Apenas administradores podem:
      - Atualizar dados de outros usuários
      - Alterar roles de usuários
      - Ativar/desativar usuários
    """
    return await user_api.update_user(user_id, user_data, current_user)