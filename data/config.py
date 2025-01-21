"""
Database Configuration Module

Gerencia as configurações de conexão com o banco de dados.
"""

import os
from typing import Dict
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class DatabaseConfig:
    """Gerencia configurações do banco de dados"""
    
    @staticmethod
    def get_config() -> Dict[str, str]:
        """
        Retorna as configurações do banco de dados.

        Returns:
            Dict[str, str]: Configurações de conexão
        """
        return {
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT")
        }