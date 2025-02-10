# __init__.py
"""Database schemas initialization module"""

from .tables import TABLE_SCHEMAS, execute_tables
from .keys import SQL_SCRIPTS as KEY_SCRIPTS, execute_keys
from .views import SQL_SCRIPTS as VIEW_SCRIPTS, execute_scripts as execute_views

__all__ = [
    'TABLE_SCHEMAS',
    'KEY_SCRIPTS',
    'VIEW_SCRIPTS',
    'execute_tables',
    'execute_keys',
    'execute_views'
]