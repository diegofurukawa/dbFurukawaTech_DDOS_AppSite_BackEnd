"""
Utils Package

Este pacote fornece utilitários e ferramentas de uso geral para o projeto.
"""

from .log import create_logger
# from .geoip_manager import GeoIPManager
# from .search_country import get_country_for_ip, search_multiple_ips

__all__ = [
    'create_logger',
]