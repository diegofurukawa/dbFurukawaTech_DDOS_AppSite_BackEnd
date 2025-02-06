"""
Database Configuration Module

Gerencia as configurações de conexão com o banco de dados.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class DatabaseConfig:
    """Gerencia configurações do banco de dados"""
    
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """
        Retorna as configurações do banco de dados.

        Returns:
            Dict[str, Any]: Configurações de conexão e pool
        """
        return {
            # Configurações básicas de conexão
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            
            # Configurações do pool
            "minconn": int(os.getenv("DB_POOL_MIN_CONN", "1")),
            "maxconn": int(os.getenv("DB_POOL_MAX_CONN", "20")),
            
            # Configurações de timeout e keepalive
            "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "30")),
            "keepalives": int(os.getenv("DB_KEEPALIVES", "1")),
            "keepalives_idle": int(os.getenv("DB_KEEPALIVES_IDLE", "30"))
        }