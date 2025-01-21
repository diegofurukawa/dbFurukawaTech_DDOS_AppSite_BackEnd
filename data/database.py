"""
Database Module

Módulo responsável pelo gerenciamento de conexões e operações com o banco de dados PostgreSQL.
Fornece funcionalidades para criar tabelas, inserir e atualizar dados.
"""

import psycopg2
import json
from psycopg2 import OperationalError
import os
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from dotenv import load_dotenv

from utils.log import create_logger
from .schemas import TABLE_SCHEMAS
from .config import DatabaseConfig

# Configuração do logger
module_logger = create_logger("database")

class DatabaseConnection:
    """Gerenciador de conexão com o banco de dados"""
    
    def __init__(self):
        """Inicializa o gerenciador de banco de dados"""
        self.logger = module_logger.getChild(self.__class__.__name__)
        self.connection = None
        self.config = DatabaseConfig.get_config()

    def connect(self) -> None:
        """
        Estabelece conexão com o banco de dados.
        
        Raises:
            OperationalError: Se houver erro na conexão
        """
        try:
            self.connection = psycopg2.connect(**self.config)
            self.logger.info("Conexão ao banco de dados PostgreSQL estabelecida")
        except OperationalError as e:
            self.logger.error(
                f"Erro ao conectar ao banco de dados: {e}\n"
                f"Host: {self.config['host']}, "
                f"Port: {self.config['port']}, "
                f"Database: {self.config['database']}, "
                f"User: {self.config['user']}"
            )
            raise

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        Executa uma query SQL genérica.

        Args:
            query: Query SQL a ser executada
            params: Parâmetros para a query (opcional)

        Returns:
            List[Tuple]: Resultados da query

        Raises:
            Exception: Se houver erro na execução
        """
        if not self.connection:
            raise Exception("Conexão com o banco de dados não está aberta")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                self.logger.info("Query executada com sucesso")
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Erro ao executar query: {e}")
            self.connection.rollback()
            raise

    def close(self) -> None:
        """Fecha a conexão com o banco de dados"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.info("Conexão com o banco de dados fechada")

    def __enter__(self) -> 'DatabaseConnection':
        """Suporte para uso com context manager"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha conexão ao sair do context manager"""
        self.close()


class DataBaseWS:
    """
    Classe principal para operações com o banco de dados.
    Gerencia conexões, tabelas e operações CRUD.
    """

    def __init__(self):
        """Inicializa o gerenciador de banco de dados"""
        self.logger = module_logger.getChild(self.__class__.__name__)
        self.connection = None
        self.config = DatabaseConfig.get_config()

    def connect(self) -> None:
        """
        Estabelece conexão e inicializa as tabelas.
        
        Raises:
            OperationalError: Se houver erro na conexão
        """
        try:
            self.connection = psycopg2.connect(**self.config)
            self.logger.info("Conexão ao banco de dados PostgreSQL estabelecida")
            self.create_tables()
        except OperationalError as e:
            self.logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def create_tables(self) -> None:
        """Cria as tabelas necessárias se não existirem"""
        if not self.connection:
            self.logger.error("Não é possível criar tabelas sem uma conexão válida")
            return

        with self.connection.cursor() as cursor:
            for table_name, create_table_query in TABLE_SCHEMAS.items():
                try:
                    cursor.execute(create_table_query)
                    self.connection.commit()
                    self.logger.info(f"Tabela '{table_name}' criada/verificada com sucesso")
                except Exception as e:
                    self.logger.error(f"Erro ao criar tabela '{table_name}': {e}")
                    self.connection.rollback()

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        Executa uma query SQL genérica.

        Args:
            query: Query SQL a ser executada
            params: Parâmetros para a query (opcional)

        Returns:
            List[Tuple]: Resultados da query

        Raises:
            Exception: Se houver erro na execução
        """
        if not self.connection:
            raise Exception("Conexão com o banco de dados não está aberta")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                self.logger.info("Query executada com sucesso")
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Erro ao executar query: {e}")
            self.connection.rollback()
            raise

    def _sanitize_data(self, data: Dict[str, Any], columns: List[str]) -> Dict[str, Any]:
        """
        Sanitiza os dados para inserção no banco.

        Args:
            data: Dicionário de dados
            columns: Lista de colunas

        Returns:
            Dict[str, Any]: Dados sanitizados
        """
        sanitized = {}
        for col in columns:
            value = data.get(col)
            if isinstance(value, dict):
                sanitized[col] = json.dumps(value)
            elif isinstance(value, bool):
                sanitized[col] = value
            elif value is None:
                sanitized[col] = None
            else:
                sanitized[col] = str(value)
        return sanitized

    def insert_alert(self, alert_data: Dict[str, Any]) -> None:
        """
        Insere ou atualiza um alerta no banco de dados.

        Args:
            alert_data: Dados do alerta a ser inserido/atualizado
        """
        columns = [
            'alert_id', 'alert_type', 'start_time', 'stop_time', 'duration',
            'max_impact_bps', 'max_impact_pps', 'ongoing', 'importance', 'mo_gid',
            'mo_name', 'mo_misusesig', 'host_address', 'ip_version', 'isFastDetected',
            'direction', 'device_gid', 'device_name', 'threshold', 'severity_pct',
            'unit', 'max_impact_boundary', 'mo_importance', 'misusetypes',
            'mimpact_bps', 'country', 'updated_at'
        ]

        sanitized_data = self._sanitize_data(alert_data, columns)

        placeholders = [f"%({col})s" for col in columns]
        columns_str = ", ".join(columns)
        placeholders_str = ", ".join(placeholders)
        update_str = ", ".join(f"{col} = EXCLUDED.{col}" for col in columns)

        query = f"""
        INSERT INTO alerts ({columns_str})
        VALUES ({placeholders_str})
        ON CONFLICT (alert_id) DO UPDATE SET
        {update_str}
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, sanitized_data)
                self.connection.commit()
                self.logger.info(f"Alerta {sanitized_data['alert_id']} inserido/atualizado")
        except Exception as e:
            self.logger.error(f"Erro ao inserir/atualizar alerta: {e}")
            self.connection.rollback()

    def insert_mitigation(self, mitigation_data: Dict[str, Any]) -> None:
        """
        Insere ou atualiza uma mitigação no banco de dados.

        Args:
            mitigation_data: Dados da mitigação a ser inserida/atualizada
        """
        if not self.connection:
            raise Exception("Conexão com o banco de dados não está aberta")

        columns = [
            'mitigation_id', 'name', 'subtype', 'auto', 'type', 'type_name',
            'config_id', 'prefix', 'alert_id', 'degraded', 'user_mitigation',
            'is_automitigation', 'ip_version', 'flist_gid', 'is_learning',
            'learning_cancelled', 'mo_name', 'mo_gid', 'duration', 'ongoing',
            'start_time', 'stop_time'
        ]

        sanitized_data = self._sanitize_data(mitigation_data, columns)

        placeholders = [f"%({col})s" for col in columns]
        columns_str = ", ".join(columns + ['updated_at'])
        placeholders_str = ", ".join(placeholders + ['CURRENT_TIMESTAMP'])
        update_str = ", ".join(f"{col} = EXCLUDED.{col}" for col in columns + ['updated_at'])

        query = f"""
        INSERT INTO mitigations ({columns_str})
        VALUES ({placeholders_str})
        ON CONFLICT (mitigation_id) DO UPDATE SET
        {update_str}
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, sanitized_data)
                self.connection.commit()
                self.logger.info(
                    f"Mitigação {sanitized_data['mitigation_id']} "
                    "inserida/atualizada"
                )
        except Exception as e:
            self.logger.error(f"Erro ao inserir/atualizar mitigação: {e}")
            self.connection.rollback()

    def insert_managed_object(self, mo_data: Dict[str, Any]) -> None:
        """
        Insere ou atualiza um objeto gerenciado no banco de dados.

        Args:
            mo_data: Dados do objeto gerenciado
        """
        # Prepara e sanitiza os dados
        prepared_data = mo_data.copy()
        self._prepare_managed_object_data(prepared_data)
        sanitized_data = self._sanitize_data(prepared_data, prepared_data.keys())

        keys = list(sanitized_data.keys())
        values = [sanitized_data[key] for key in keys]
        placeholders = ", ".join(["%s"] * len(keys))
        columns = ", ".join(keys)
        update_stmt = ", ".join([f"{key} = EXCLUDED.{key}" for key in keys])

        query = f"""
        INSERT INTO managedobjects ({columns})
        VALUES ({placeholders})
        ON CONFLICT (id) DO UPDATE SET
        {update_stmt}
        """

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                self.connection.commit()
                self.logger.info(
                    f"Objeto gerenciado {mo_data['id']} inserido/atualizado"
                )
        except Exception as e:
            self.logger.error(
                f"Erro ao inserir/atualizar objeto gerenciado: {e}\n"
                f"Query: {query}\n"
                f"Valores: {values}"
            )
            self.connection.rollback()
            raise

    @staticmethod
    def _prepare_managed_object_data(mo_data: Dict[str, Any]) -> None:
        """
        Prepara os dados do objeto gerenciado para inserção.

        Args:
            mo_data: Dados a serem preparados
        """
        # Converte campos vazios para None em campos booleanos
        boolean_fields = [
            'autodetected', 'treat_external_as_internal', 'automitigation_profiled',
            'automitigation_learned_prefixes', 'automitigation_learned_prefixes_mitigate_on_query_failure',
            'automitigation_tms_enabled', 'automitigation_tms_reuse', 'blackhole_auto_enabled',
            'flowspec_auto_enabled', 'sightline_signaling_auto_enabled', 'match_dark',
            'match_enabled', 'dynamic_match_enabled', 'dynamic_match_multitenant_enabled',
            'profiled_use_snmp', 'require_targeted_cs_requests_evaluated'
        ]
        
        for field in boolean_fields:
            if mo_data.get(field) == '':
                mo_data[field] = None

        # Converte campos vazios para 0 em campos numéricos
        numeric_fields = [
            'tiered_blackhole_tms_bps', 'tiered_blackhole_tms_pps',
            'profiled_incoming_bps', 'profiled_incoming_pps',
            'profiled_outgoing_bps', 'profiled_outgoing_pps',
            'bandwidth_threshold', 'pps_threshold', 'protocol_threshold',
            'num_children', 'automitigation_stop_minutes', 'blackhole_auto_stop_minutes',
            'profiled_severity_duration', 'host_severity_duration'
        ]
        
        for field in numeric_fields:
            if mo_data.get(field) == '':
                mo_data[field] = 0

    def close(self) -> None:
        """Fecha a conexão com o banco de dados"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.info("Conexão com o banco de dados fechada")

    def __del__(self) -> None:
        """Destrutor da classe"""
        self.close()
