"""
Data Saver Module

Este módulo fornece funcionalidades para salvar dados em diferentes formatos,
como CSV e TXT. Suporta dados em formato DataFrame, listas e dicionários.
"""

import os
import csv
import json
import pandas as pd
from typing import Any, List, Dict, Union, Optional
from pathlib import Path
from enum import Enum

from utils.log import create_logger

# Configuração do logger
module_logger = create_logger("data_saver")

class OutputFormat(Enum):
    """Formatos de saída suportados"""
    CSV = 'csv'
    TXT = 'txt'

    @classmethod
    def get_supported_formats(cls) -> List[str]:
        """Retorna lista de formatos suportados"""
        return [format.value for format in cls]


class DataSaverError(Exception):
    """Exceção customizada para erros do DataSaver"""
    pass


class DataSaver:
    """
    Classe responsável por salvar dados em diferentes formatos.
    Suporta salvamento em CSV e TXT com diferentes tipos de dados.
    """

    def __init__(self, output_format: str, output_directory: str):
        """
        Inicializa o DataSaver.

        Args:
            output_format: Formato de saída ('csv' ou 'txt')
            output_directory: Diretório onde os arquivos serão salvos

        Raises:
            ValueError: Se o formato de saída não for suportado
        """
        self.logger = module_logger.getChild(self.__class__.__name__)
        
        # Validação do formato de saída
        if output_format not in OutputFormat.get_supported_formats():
            raise ValueError(
                f"Formato não suportado: {output_format}. "
                f"Formatos suportados: {OutputFormat.get_supported_formats()}"
            )
        
        self.output_format = output_format
        self.output_directory = output_directory
        self.ensure_output_directory()
        
        self.logger.info(
            f"DataSaver inicializado com formato: {self.output_format}, "
            f"diretório: {self.output_directory}"
        )

    def ensure_output_directory(self) -> None:
        """
        Garante que o diretório de saída existe.

        Raises:
            DataSaverError: Se houver erro ao criar o diretório
        """
        if not self.output_directory:
            self.logger.warning("Diretório de saída não definido. Usando diretório atual.")
            self.output_directory = "."

        try:
            Path(self.output_directory).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Diretório de saída verificado: {self.output_directory}")
        except OSError as e:
            error_msg = f"Erro ao criar diretório de saída: {str(e)}"
            self.logger.error(error_msg)
            raise DataSaverError(error_msg)

    def save_data(self, data: Any, filename: str) -> None:
        """
        Salva dados no formato especificado.

        Args:
            data: Dados a serem salvos (DataFrame, lista ou dicionário)
            filename: Nome do arquivo (sem extensão)

        Raises:
            DataSaverError: Se houver erro ao salvar os dados
            ValueError: Se o formato não for suportado
        """
        self.logger.info(f"Iniciando salvamento dos dados como {self.output_format}")
        
        try:
            if self.output_format == OutputFormat.CSV.value:
                self.save_as_csv(data, filename)
            elif self.output_format == OutputFormat.TXT.value:
                self.save_as_txt(data, filename)
            else:
                raise ValueError(f"Formato não suportado: {self.output_format}")
                
        except Exception as e:
            error_msg = f"Erro ao salvar dados: {str(e)}"
            self.logger.error(error_msg)
            raise DataSaverError(error_msg)

    def save_as_csv(self, data: Union[pd.DataFrame, List], filename: str) -> None:
        """
        Salva dados em formato CSV.

        Args:
            data: DataFrame ou lista de dados
            filename: Nome do arquivo

        Raises:
            TypeError: Se o tipo de dados não for suportado
            DataSaverError: Se houver erro ao salvar
        """
        filepath = Path(self.output_directory) / f"{filename}.csv"
        
        try:
            if isinstance(data, pd.DataFrame):
                data.to_csv(filepath, index=False)
                
            elif isinstance(data, list):
                if data and isinstance(data[0], dict):
                    self._save_dict_list_as_csv(data, filepath)
                else:
                    self._save_simple_list_as_csv(data, filepath)
                    
            else:
                raise TypeError(
                    "Dados devem ser DataFrame ou lista. "
                    f"Tipo recebido: {type(data)}"
                )
            
            self.logger.info(f"Dados salvos com sucesso em CSV: {filepath}")
            
        except Exception as e:
            error_msg = f"Erro ao salvar CSV: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise DataSaverError(error_msg)

    def save_as_txt(self, data: Union[pd.DataFrame, List, Any], filename: str) -> None:
        """
        Salva dados em formato TXT.

        Args:
            data: Dados a serem salvos
            filename: Nome do arquivo

        Raises:
            DataSaverError: Se houver erro ao salvar
        """
        filepath = Path(self.output_directory) / f"{filename}.txt"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                if isinstance(data, pd.DataFrame):
                    data.to_string(file, index=False)
                    
                elif isinstance(data, list):
                    if data and isinstance(data[0], dict):
                        json.dump(data, file, indent=2)
                    else:
                        for item in data:
                            file.write(f"{item}\n")
                            
                else:
                    file.write(str(data))
            
            self.logger.info(f"Dados salvos com sucesso em TXT: {filepath}")
            
        except Exception as e:
            error_msg = f"Erro ao salvar TXT: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            raise DataSaverError(error_msg)

    def _save_dict_list_as_csv(self, data: List[Dict], filepath: Path) -> None:
        """
        Salva lista de dicionários em CSV.

        Args:
            data: Lista de dicionários
            filepath: Caminho do arquivo
        """
        keys = data[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    def _save_simple_list_as_csv(self, data: List, filepath: Path) -> None:
        """
        Salva lista simples em CSV.

        Args:
            data: Lista de dados
            filepath: Caminho do arquivo
        """
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    @staticmethod
    def validate_data_format(data: Any) -> bool:
        """
        Valida se o formato dos dados é suportado.

        Args:
            data: Dados a serem validados

        Returns:
            bool: True se o formato for válido
        """
        return (
            isinstance(data, pd.DataFrame) or
            isinstance(data, list) or
            isinstance(data, dict)
        )