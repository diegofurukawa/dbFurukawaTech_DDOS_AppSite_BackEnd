from datetime import datetime, timedelta
import os
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from data.database import DatabaseConnection
from dotenv import load_dotenv
from utils.log import create_logger

# Load environment variables
load_dotenv()

# Configure logger
logger = create_logger("auth")

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set in environment variables")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha está correta, primeiro tentando usar o CryptContext,
    e se falhar, tenta diretamente com bcrypt
    """
    logger.info("Attempting to verify password")
    try:
        # Primeira tentativa usando CryptContext
        result = pwd_context.verify(plain_password, hashed_password)
        logger.info("Password verification successful using CryptContext")
        return result
    except Exception as e:
        logger.warning(f"CryptContext verification failed: {str(e)}")
        try:
            # Fallback para bcrypt direto
            import bcrypt
            result = bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
            logger.info("Password verification successful using bcrypt directly")
            return result
        except Exception as e:
            logger.error(f"Password verification failed with bcrypt: {str(e)}")
            return False

def get_password_hash(password: str) -> str:
    """
    Gera um hash seguro para a senha fornecida
    """
    logger.info("Generating password hash")
    try:
        hashed = pwd_context.hash(password)
        logger.info("Password hash generated successfully")
        return hashed
    except Exception as e:
        logger.error(f"Error generating password hash: {str(e)}")
        raise

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token de acesso JWT
    """
    logger.info("Creating access token")
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info("Access token created successfully")
        return token
    except Exception as e:
        logger.error(f"Error creating access token: {str(e)}")
        raise

def create_refresh_token(data: dict) -> str:
    """
    Cria um token de atualização JWT
    """
    logger.info("Creating refresh token")
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info("Refresh token created successfully")
        return token
    except Exception as e:
        logger.error(f"Error creating refresh token: {str(e)}")
        raise

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Valida o token JWT e retorna o usuário atual
    """
    logger.info("Validating user token")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodifica o token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.error("Token payload does not contain email")
            raise credentials_exception
            
        # Busca o usuário no banco de dados
        with DatabaseConnection() as db:
            result = db.execute_query(
                "SELECT * FROM users WHERE email = %s AND active = true",
                (email,)
            )
            if not result:
                logger.error(f"No active user found for email: {email}")
                raise credentials_exception
                
            # Mapeia os resultados da query para um dicionário
            user_data = dict(zip(
                ['idUser', 'email', 'name', 'password_hash', 'company', 'role', 
                 'active', 'createdAt', 'last_login'],
                result[0]
            ))
            logger.info(f"User authenticated successfully: {email}")
            return user_data
            
    except JWTError as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error in user validation: {str(e)}")
        raise credentials_exception