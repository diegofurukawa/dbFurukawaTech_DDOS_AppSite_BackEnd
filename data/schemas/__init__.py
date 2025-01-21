# __init__.py (dentro da pasta schemas)
"""Database schemas initialization module"""

from .alerts import ALERTS_SCHEMA
from .mitigations import MITIGATIONS_SCHEMA
from .managed_objects import MANAGED_OBJECTS_SCHEMA

TABLE_SCHEMAS = {
    "alerts": ALERTS_SCHEMA,
    "mitigations": MITIGATIONS_SCHEMA,
    "managed_objects": MANAGED_OBJECTS_SCHEMA
}

__all__ = [
    'TABLE_SCHEMAS',
    'ALERTS_SCHEMA',
    'MITIGATIONS_SCHEMA',
    'MANAGED_OBJECTS_SCHEMA'
]